#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import re
import argparse
import itertools

import logging
import unittest

VERSION = "1.0.0"

MATHCOMMANDS = " ".join([
    "prime in times plus dual dots dim supp subset deg ker star perp rk emptyset sum quad",
    r"eq.not(\neq) gt.eq(\geq) lt.eq(\leq) arrow.bar(\mapsto) infinity eq(=) lt(<) gt(>)",
    r"union(\cup) union.big(\bigcup) union.sq(\sqcup) union.big.sq(\bigsqcup) sect(\cap) sect.big(\bigcap) forall",
    r">>(\gg) <<(\ll) <=>(\iff) dot(\cdot) =>(\implies)",
    r"times.circle(\otimes) times.square(\boxtimes) plus.circle(\oplus) plus.circle.big(\bigoplus) tilde.op(\sim) compose(\circ)",
    r"angle.l(\langle) angle.r(\rangle) arrow.squiggly(\rightsquigarrow)",
    "alpha Alpha beta Beta gamma Gamma delta Delta epsilon Epsilon zeta Zeta eta Eta theta Theta iota Iota kappa Kappa lambda Lambda",
    "mu Mu nu Nu xi Xi omicron Omicron pi Pi rho Rho sigma Sigma tau Tau upsilon Upsilon phi Phi chi Chi psi Psi omega Omega",
    "AA CC FF OO PP QQ ZZ cA cB cL",
    r"cal(\mathcal{}) frak(\mathfrak{}) hat(\widehat{}) tilde(\widetilde{}) overline(\overline{})",
    r"binom(\binom{}) frac(\frac{}) mat(\matrix{}) text(\text{})",
    # personal commands
    "Dbcoh Hom Ext RHom RGamma Coh QCoh intRHom bullet Cone qis Pic rdim emptyperp",
    "iso caniso isoarrow monoarrow epiarrow",
])

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


def truncate_newlines(s):
    start = 0
    end = len(s)
    while len(s) > start and s[start] == '\n':
        start += 1
    while end > 0 and s[end-1] == '\n':
        end -= 1
    return s[start:end]

def read_math_commands():
    return MATHCOMMANDS.split()


class TestCommaSplitting(unittest.TestCase):
    atoms = ['a', '4', '112 + 12', 'f(2)', '(x, y)', 'f(x, y) + g(1, h(2, 3))']
    def test_atoms(self):
        for atom in self.atoms:
            with self.subTest(case=atom):
                self.assertEqual(len(get_top_level_commas(atom)), 0)
    def test_3_joins(self):
        atom_sets = itertools.combinations(self.atoms, 3)
        for atom_set in atom_sets:
            s = ", ".join(list(atom_set))
            with self.subTest(case=s):
                commas = get_top_level_commas(s)
                self.assertEqual(len(commas), 2)
                for comma in commas:
                    self.assertEqual(s[comma], ',')

def get_top_level_commas(s: str, symbols: list[str] = [',']) -> list[int]:
    r"""
    This function figures out which commas in the string `s` are not inside of pairs of parentheses, brackets, etc,
    in order to split strings like `a, b, f(x, y), g(1, 2) + h(4, g(5, 2))` into separate items without cutting `f(x, y)` into
    two parts.
    Returns a list of indices of top level commas in `s`.
    """
    i = 0
    enclosings = []
    top_level_commas = []
    while i < len(s):
        if s[i] in symbols and len(enclosings) == 0:
                top_level_commas.append(i)
        elif s[i] == '"':
            if len(enclosings) > 0 and enclosings[-1] == '"':
                enclosings = enclosings[:-1]
            else:
                enclosings.append('"')
        elif s[i] == "'":
            if len(enclosings) > 0 and enclosings[-1] == "'":
                enclosings = enclosings[:-1]
            else:
                enclosings.append("'")
        elif s[i] in ['(', '{', '[']:
            enclosings.append(s[i])
        elif s[i] in [')', '}', ']']:
            assert(len(enclosings) > 0)
            enclosings = enclosings[:-1]
        i += 1
    return top_level_commas

def whitespace_around_character(s: str, i: int) -> tuple[int, int]:
    r"""
    Returns i_1, i_2 such that `i` is between `i1` and `i2` and `s[i_1:i_2]` is a substring consisting of whitespace, then 
    the `i`'th character, then again whitespace.
    """
    i1 = i
    while i1 >= 0 and s[i1-1].isspace():
        i1 -= 1
    i2 = i+1
    while i2 < len(s) and s[i2].isspace():
        i2 += 1
    return i1, i2

class TestSlashifyCommand(unittest.TestCase):
    def test_inline_matrices(self):
        cases = [
            ("mat(1, 2; 3, 4)", r"\left(\begin{matrix} 1 & 2 \\ 3 & 4 \end{matrix}\right)"),
            ("mat(1, 2)", r'\left(\begin{matrix} 1 & 2 \end{matrix}\right)'),
            ("mat(1; 2)", r'\left(\begin{matrix} 1 \\ 2 \end{matrix}\right)'),
            ("mat(1)", r'\left(\begin{matrix} 1 \end{matrix}\right)'),
            ("mat(f(x, y), a + f(c, d); 0, m(x, m(y; z)))", r"\left(\begin{matrix} f(x, y) & a + f(c, d) \\ 0 & m(x, m(y; z)) \end{matrix}\right)"),
        ]
        for case in cases:
            with self.subTest(case=case):
                args, expected = case
                text = '$' + args + '$'
                math_mode_mask = parse_math_mode_mask(text)
                self.assertEqual('$' + expected + '$', math_slashify(text, math_mode_mask, commands=['mat(\mat{})']))
    def test_indented_matrices(self):
        cases = [
            ('''
  1, 2;
  3, 4
''', r'''\left(\begin{matrix}
  1 & 2 \\
  3 & 4
\end{matrix}\right)'''),
            ('''
    1, 2;
    3, 4
  ''', r'''\left(\begin{matrix}
    1 & 2 \\
    3 & 4
  \end{matrix}\right)'''),
        ]
        for case in cases:
            with self.subTest(case=case):
                args, expected = case
                text = '$prefix + mat(' + args + ')$'
                math_mode_mask = parse_math_mode_mask(text)
                self.assertEqual('$prefix + ' + expected + '$', math_slashify(text, math_mode_mask, commands=['mat(\mat{})']))

def handle_special_argument_lists(text: str, typst_command: str, command_start: int, command_end: int, bracket_opens: int, bracket_closes: int):
    r"""
    Converts typst-style argument list for `text` and `mat` commands in math mode to their LaTeX equivalents.
    The `text` command is here purely because it can be used in two ways: `text[abc]` and `text([abc])`.
    """
    args_start = bracket_opens + 1
    args_end = bracket_closes
    replacements = []
    if typst_command == 'text':
        if command_start > 0 and text[command_start-1] == '#':
            command_start -= 1
        replacements.append(((command_start, command_end), r'\text'))

        bracket_opens_end = bracket_opens + 1
        if text[bracket_opens] == '(' and text[bracket_opens+1] == '[':
            bracket_opens_end += 1
        replacements.append(((bracket_opens, bracket_opens_end), '{'))

        bracket_closes_start = bracket_closes
        if text[bracket_closes] == ')' and text[bracket_closes-1] == ']':
            bracket_closes_start -= 1
        replacements.append(((bracket_closes_start, bracket_closes+1), '}'))
    elif typst_command == 'mat':
        args = text[args_start:args_end]
        row_separators = [ semicolon_pos + args_start for semicolon_pos in get_top_level_commas(args, symbols=[';']) ]
        row_ranges = []
        if len(row_separators) > 0:
            row_ranges.append((args_start, row_separators[0]))
            row_ranges += [ (row_separators[i], row_separators[i+1]) for i in range(len(row_separators) - 1) ]
            row_ranges.append((row_separators[-1], args_end))
        else:
            row_ranges = [(args_start, args_end)]
        rows_commas = []
        for row_start, row_end in row_ranges:
            row = text[row_start:row_end]
            rows_commas.append([ comma_pos + row_start for comma_pos in get_top_level_commas(row) ])
        
        for semicolon_pos in row_separators:
            replacements.append(((semicolon_pos, semicolon_pos+1), r' \\'))
        for commas_list in rows_commas:
            for comma_pos in commas_list:
                replacements.append(((comma_pos, comma_pos+1), r' &'))
        need_space_after_start = not text[bracket_opens+1].isspace()
        replacements.append(((command_start, bracket_opens+1), r'\left(\begin{matrix}' + (' ' if need_space_after_start else '')))
        need_space_before_end = not text[bracket_closes-1].isspace()
        replacements.append(((bracket_closes, bracket_closes+1), (' ' if need_space_before_end else '') + r'\end{matrix}\right)'))
    else:
        raise NotImplementedError(f"Unknown special command passed: {typst_command}!")
    return replacements

def math_slashify(text: str, math_mode_mask: list[bool], commands: list[str]):
    r"""
    math_slashify changes typst syntax for math commands to LaTeX-style syntax.
    It only handles math commands specified in the `commands` list! The list is not a verbatim
    list of commands, there is some special syntax for smarter replacements:
    - if a string `times` is in `commands`, math_slashify will replace, e.g., $3 times 3$ (typst) with $3 \times 3$ (LaTeX).
    - user can specify a better LaTeX equivalent by using parentheses: if a string `gt.eq(\geq)` appears in the `commands` list,
      typst command `gt.eq` will be replaced by `\geq` instead of `\gt.eq`. Note that a command `gt` will not be matched 
      by `gt.eq` or `eq.gt` (if the latter existed).
    - This function can also change parentheses to brackets when the command accepts arguments. This also needs to be specifically
      requested by a magic syntax involving brackets '{}' in the `commands` list. For example, if a string `frac(\mathfrak{})` (note
      the '{}' after the function name) appears in the `commands` list, math_slashify will transform `2 + frac(m)` to `2 + \mathfrak{m}`.
    """
    replacements = []
    commands_with_special_arguments = ['mat', 'text']
    for command in commands:
        command_typst = command
        command_tex = '\\' + command
        replace_brackets = False
        if command.find('(') != -1:
            assert(command[-1] == ')')
            paren = command.find('(')
            command_typst = command[:paren]
            command_tex = command[paren+1:-1]
            if len(command_tex) > 2 and command_tex[-2] == '{' and command_tex[-1] == '}':
                command_tex = command_tex[:-2]
                replace_brackets = True
        for m in re.finditer('(?<!(.[a-zA-Z]|[a-zA-Z]\\.))' + command_typst + '(?!([a-zA-Z].|\\.[a-zA-Z]))', text):
            start, end = m.span()
            if not math_mode_mask[start]:
                continue
            if replace_brackets and end < len(text) and (text[end] == '(' or text[end] == '['):
                bracket_opens = end
                bracket_closes = find_closing_bracket(text, bracket_opens)
                args_start = bracket_opens + 1
                args = text[args_start:bracket_closes]
                if command_typst not in commands_with_special_arguments:
                    replacements.append(((start, end), command_tex))
                    replacements.append(((bracket_opens, bracket_opens+1), '{'))
                    replacements.append(((bracket_closes, bracket_closes+1), '}'))
                    # Here we handle basic commands with multiple arguments, e.g., `binom(3, 2)` -> `\binom{3}{2}`
                    top_level_commas = [ pos + args_start for pos in get_top_level_commas(args) ]
                    for comma_pos in top_level_commas:
                        pre_comma, post_comma = whitespace_around_character(text, comma_pos)
                        replacements.append(((pre_comma, post_comma), '}{'))
                else:
                    replacements += handle_special_argument_lists(text, command_typst, start, end, bracket_opens, bracket_closes)
            else:
                replacements.append(((start, end), command_tex))
    new_text = apply_replacements(text, replacements)
    return new_text

def find_closing_bracket(text: str, bracket_opens: int, single_line_mode: bool = False) -> int:
    r"""
    find_closing_bracket returns an index i such that text[i] is one of ')', ']', '}', such that:
    - i comes strictly after the symbol text[bracket_opens];
    - the text fragment text[bracket_opens+1:i] has balanced parenthesis.
    This function throws an exception when such i cannot be found (so, when `text` is not a balanced string).

    For example, in a string "#underline([Test (case)])" the result of find_closing_bracket with bracket_opens at 10
    (the index of '(' after 'underline')) is the index of the final closing parenthesis.
    """
    opened = 1
    cur = bracket_opens + 1
    while cur < len(text):
        if text[cur] in ['(', '{', '[']:
            opened += 1
        elif text[cur] in [')', '}', ']']:
            opened -= 1
            if opened == 0:
                break
        if single_line_mode and text[cur] == '\n':
            raise ValueError(f"looked for matching parenthesis in a single_line_mode, but a line break came first: {text[bracket_opens:cur]}")
        cur += 1
    if cur == len(text):
        raise ValueError(f"looked for closing parenthesis, found end of text: {text[bracket_opens:max(len(text), min(cur, bracket_opens + 100))]}")
    return cur


def math_rebrace_sub_sup(text: str, math_mode_mask: list[bool]):
    r"""
    math_rebrace_sub_sup converts parentheses around the subscripts/supscripts in typst math mode
    to braces as required by TeX: e.g., $a_(1, 2) + b^(cd)$ is converted to $a_{1, 2} + b^{cd}$.
    """
    assert(len(math_mode_mask) == len(text))
    new_text = ''
    parentheses_spans = []

    prefixes = [('_', r'(?<!\s)', 1), (r'\^', r'(?<!\s)', 1)]
    for prefix, preregexp, length in prefixes:
        regexp = preregexp + prefix + r'\('
        for m in re.finditer(regexp, text):
            start, end = m.span()
            if not math_mode_mask[start]:
                continue
            open_paren = start+length
            paren_closes = find_closing_bracket(text, open_paren)
            parentheses_spans.append((open_paren, paren_closes))
    new_text_list = list(text)
    for start, end in parentheses_spans:
        new_text_list[start] = '{'
        new_text_list[end] = '}'
    new_text = "".join(new_text_list)
    return new_text

def parse_bibliography(bibtext: str) -> list[str]:
    r"""
    parse_bibliography accepts the contents of a .bib file and produces a list of labels from it.
    """
    pattern = r'^\s*@\s*[a-zA-Z]+\s*{\s*([0-9a-zA-Z_\-]+)\s*,'
    bib_refs = []
    for m in re.finditer(pattern, bibtext, re.MULTILINE):
        bib_refs.append(m.groups()[0])
    return bib_refs

def refs_texify(text: str, bib_refs: list[str], autoref_mode: bool = False, supplement_implies_bibref: bool = True):
    r"""
    refs_texify replaces typst references via @something
    by either \ref{} or \cite{} depending on whether the argument appears
    in the user-provided list `bib_refs`. If a reference has a supplement, it is by default
    also assumed to be a bibliography reference. Also replaces `#cite` commands.
    """
    at_signs_list = list(map(lambda m: m.span()[0], re.finditer(r'(?<!\w)@', text)))
    allowed_symbols = ['_', ':', '-']
    replacements = []
    for i in at_signs_list:
        ref_name_ends = i+1
        supplement = None
        while ref_name_ends < len(text) and (text[ref_name_ends].isalnum() or text[ref_name_ends] in allowed_symbols):
            ref_name_ends += 1
        # Labels don't normally end on colons or hyphens. Typst parser can handle this correctly because it has access
        # to the full list of labels in the document, but we can't, hence this workaround.
        while text[ref_name_ends-1] == ':' or text[ref_name_ends-1] == '-':
            ref_name_ends -= 1
        assert(ref_name_ends > i+1)
        ref_name = text[i+1:ref_name_ends]
        ref_ends = ref_name_ends
        if text[ref_name_ends] == '[':
            supplement_starts = ref_name_ends+1
            supplement_ends = find_closing_bracket(text, ref_name_ends)
            ref_ends = supplement_ends + 1
            supplement = text[supplement_starts: supplement_ends]
        replacement = ''
        if ref_name in bib_refs:
            if supplement is None:
                replacement = r'\cite{' + ref_name + r'}'
            else:
                replacement = r'\cite[' + supplement + r']{' + ref_name + r'}'
        else:
            replacement = r'\ref{' + ref_name + r'}'
            if supplement is not None:
                if supplement_implies_bibref:
                    replacement = r'\cite[' + supplement + r']{' + ref_name + r'}'
                else:
                    raise ValueError(f"found an @reference with a supplement which does not seem to come from bibliography: {text[i:ref_ends]}")
        replacements.append(((i, ref_ends), replacement))
    for m in re.finditer(r'#cite\(<([a-zA-Z0-9\-_:]+)>\)', text):
        start, end = m.span()
        replacements.append(((start, end), r'\cite{' + m.groups()[0] + '}'))
    for m in re.finditer(r'#cite\(<([a-zA-Z0-9\-_:]+)>, supplement:', text):
        start, supplement_next = m.span()
        supplement_starts = supplement_next
        while text[supplement_starts].isspace():
            supplement_starts += 1
        if text[supplement_starts:supplement_starts+5] == 'none)':
            replacements.append(((start, supplement_starts+5), r'\cite{' + m.groups()[0] + '}'))
        elif text[supplement_starts] == '[':
            supplement_ends = find_closing_bracket(text, supplement_starts)
            if text[supplement_ends+1] != ')':
                raise ValueError(f"Could not parse a supplement to a label: {text[start:min(len(text), supplement_ends+10)]}")
            replacements.append(((start, supplement_ends+2), r'\cite[' + text[supplement_starts+1:supplement_ends] + ']{' + m.groups()[0] + '}'))
    return apply_replacements(text, replacements)

def convert_sections(text: str, math_mode_mask: list[bool]):
    r"""
    Converts Typst-style section headers like
    == Test <sec:test>
    into equivalent LaTeX commands
    """
    tex_section_names = [r'\section', r'\subsection', r'\subsubsection']
    replacements = []
    for m in re.finditer(r'^([ \t]*)(=+) ', text, re.MULTILINE):
        start, section_name_starts = m.span()
        while text[section_name_starts].isspace():
            section_name_starts += 1
        if math_mode_mask[start]:
            continue
        indentation = m.groups()[0]
        section_level = len(m.groups()[1]) - 1
        if section_level >= len(tex_section_names):
            raise NotImplementedError(f"Only three levels of (sub)sections are supported by default, can't handle {text[start:min(len(text), section_name_starts+30)]}")
        
        line_break = text.find('\n', section_name_starts)
        assert(line_break != -1)
        section_name_ends = line_break
        while text[section_name_ends-1].isspace():
            section_name_ends -= 1

        label = None
        if text[section_name_ends-1] == '>':
            bracket_opens = text.rfind('<', start, section_name_ends-1)
            if bracket_opens == -1:
                raise ValueError(f"Cannot parse section label: {text[start:section_name_ends]}")
            label = text[bracket_opens+1:section_name_ends-1]
            section_name_ends = bracket_opens
            while text[section_name_ends-1].isspace():
                section_name_ends -= 1
        tex_equivalent = indentation + tex_section_names[section_level] + '{' + text[section_name_starts:section_name_ends] + '}\n'
        if label is not None:
            tex_equivalent += indentation + r'\label{' + label + '}\n'
        replacements.append(((start, line_break+1), tex_equivalent))
    return apply_replacements(text, replacements)



def math_quoted_text_mathrm(text: str, math_mode_mask: list[bool]):
    r"""
    math_quoted_text_mathrm replaces the typst shorthand notation $"hello" times 3$ for non-italicized
    words in math mode with the \mathrm{} call
    """
    replacements = []
    opened_quote = -1
    for i in range(len(text)):
        if not math_mode_mask[i]:
            continue
        if text[i] == '"':
            if opened_quote == -1:
                opened_quote = i
            else:
                replacements.append(((opened_quote, opened_quote+1), r'\mathrm{'))
                replacements.append(((i, i+1), r'}'))
                opened_quote = -1
    return apply_replacements(text, replacements)

def parse_math_mode_mask(text: str) -> list[bool]:
    """
    parse_math_mode_mask detects math mode regions in the provided text and
    returns a "mask" for math mode. It should work for both the typst source
    and various intermediate stages of tex conversion. WARNING: it will not do
    the right things for complicated interleavings of math-in-text-in-math.
    """
    # TODO: avoid commented out text pieces.
    math_mode_mask = [False] * len(text)
    math_delimiters = [('$', '$'), ('$$', '$$'), (r'\begin{equation}', r'\end{equation}'), (r'\(', r'\)'), (r'\[', r'\]')]
    def find_closest(text, start, substrings):
        positions = list(map(lambda s: text.find(s, start), substrings))
        closest = -1
        closest_index = -1
        for i in range(len(positions)):
            pos = positions[i]
            if closest == -1 or (closest > pos and pos != -1):
                closest = pos
                closest_index = i
        return closest, closest_index
    openers = list(map(lambda p: p[0], math_delimiters))
    closers = list(map(lambda p: p[1], math_delimiters))
    pos = 0
    while pos != -1:
        pos, i = find_closest(text, pos, openers)
        if pos != -1:
            math_starts_at = pos + len(openers[i])
            math_ends_at = text.find(closers[i], math_starts_at)
            for j in range(math_starts_at, math_ends_at):
                math_mode_mask[j] = True
            pos = math_ends_at + len(closers[i])
    # Invert math mode inside of the argument of typst `text` command
    for match in re.finditer('(?<!(.[a-zA-Z]|[a-zA-Z]\\.))' + 'text' + '(?!([a-zA-Z].|\\.[a-zA-Z]))', text):
        start, text_command_ends = match.span()
        if not math_mode_mask[start]:
            continue
        assert(text[text_command_ends] in ['(', '[', '{'])
        bracket_closes = find_closing_bracket(text, text_command_ends)
        for i in range(text_command_ends, bracket_closes):
            math_mode_mask[i] = not math_mode_mask[i]
    return math_mode_mask

def convert_underline(text: str, math_mode_mask: list[bool]):
    r"""
    Converts typst `underline` command in both text mode and math mode.
    """
    replacements = []
    for m in re.finditer(r'underline', text):
        command_start, command_end = m.span()
        if not math_mode_mask[command_start]:
            if command_start == 0 or text[command_start-1] != '#':
                continue
            # include the '#' symbol in the command text
            command_start -= 1
        if math_mode_mask[command_start] and (command_start > 0 and not text[command_start-1].isspace()):
            continue
        if text[command_end] not in ['(', '[']:
            continue
        bracket_opens = command_end
        bracket_opens_end = bracket_opens+1
        if text[bracket_opens] == '(':
            assert(text[bracket_opens+1] == '[')
            bracket_opens_end += 1
        bracket_closes = find_closing_bracket(text, bracket_opens)
        bracket_closes_start = bracket_closes
        if text[bracket_closes] == ')':
            assert(text[bracket_closes-1] == ']')
            bracket_closes_start -= 1
        replacements.append(((command_start, command_end), r'\underline'))
        replacements.append(((bracket_opens, bracket_opens_end), '{'))
        replacements.append(((bracket_closes_start, bracket_closes + 1), '}'))
    return apply_replacements(text, replacements)

def find_typst_environments(text: str):
    """
    find_typst_environments searches for fragments of the form:

    #someword(could have arguments, could have none)[
      whatever text
      you have inside
    ] <also there may or may not be a label here>

    and returns a list of dicts with informations about each environment:
    where the header is, where the closing ']' is, what are the arguments, what is the label,
    what position is the content of the environment etc.
    This function works for environments-in-environments as well, provided they are indented correctly.

    NOTE: only works for correctly-indented multiline environments, ones that should be replaced
    by \begin \end pairs in TeX! Use something else for processing in-line typst commands
    like "text #underline[is] underlined".
    """
    environments = []
    for typst_env in re.finditer(r'^( *)#([a-zA-Z_]+)(\(.*\))?\[\n', text, re.MULTILINE):
        indent_string, envname, envarg = typst_env.groups()
        indent = len(indent_string)
        line_start, line_end = typst_env.span()
        # logger.debug(f"DEBUG: found an environment {envname} at position {line_start}")
        # We assume that all multiline environments are correctly indented, so we can detect
        # the end of the argument by looking for a line ']\n' with the expected indentation
        content_start = line_end
        content_end = -1
        env_end_start = -1
        env_end_end = -1
        current_line_start = line_end
        label_name = None
        while True:
            next_newline = text.find('\n', current_line_start)
            assert(next_newline != -1) # we assume the typst source to be well-formed, with final \n if necessary
            line = text[current_line_start:next_newline]
            while len(line) > 0 and line[-1].isspace():
                line = line[:-1]
            if line == (indent_string + ']'):
                content_end = current_line_start
                env_end_start = content_end + indent
                env_end_end = env_end_start + 2 # include newline here
                break
            elif line.startswith(indent_string + '] <'):
                m = re.search(indent_string + r'\] <([0-9a-zA-Z_\-\:]+)> *$', line)
                if m is None:
                    logger.error(f"Couldn't parse label after the environment end: {line}")
                assert(m is not None)
                label_name = m.groups()[0]
                content_end = current_line_start
                env_end_start = content_end + indent
                env_end_end = current_line_start + m.span()[1] + 1 # newline not included
                break
            current_line_start = next_newline+1
        # We check that the environment contents has balanced parenthesis.
        bracket_opens = line_end - 2
        bracket_closes = env_end_start
        try:
            balanced_bracket_closes = find_closing_bracket(text, bracket_opens)
            if balanced_bracket_closes != bracket_closes:
                raise ValueError("Brackets don't match")
        except:
            logger.warning(f"Environment {envname} around ```{text[max(0, line_start-20):min(len(text), line_end+20)]}``` has unbalanced brackets inside, expect broken conversion!")
        environments.append({
            'begin_coords': (line_start + indent, line_end), # the "#someword(...)[" part at the start
            'end_coords': (env_end_start, env_end_end), # the "] <maybe label>" part at the end
            'name': envname,
            'arg': envarg[1:-1] if (envarg is not None) else None, # strip out the parentheses
            'label': label_name,
            'indent': indent_string,
            'content_indented': (content_start, content_end), # the lines between the header and the footer
            })
        pass
    return environments

def handle_environment(text: str, env):
    r'''
    Returns a list of replacements to convert a typst environment (as parsed by `find_typst_environments`) to
    a LaTeX equivalent.
    '''
    replacements = []
    env_begin = ''
    if env['arg'] is not None:
        arg = env['arg']
        if arg[0] == '[':
            arg = arg[1:-1] # by default we strip out the [] pair
        env_begin += r'\begin{' + env['name'] + '}[{' + arg + '}]\n'
    else:
        env_begin += r'\begin{' + env['name'] + '}\n'
    if env['label'] is not None:
        env_begin += env['indent'] + '  ' + r'\label{' + env['label'] + '}\n'
    env_end = r'\end{' + env['name'] + '}\n'
    replacements.append((env['begin_coords'], env_begin))
    replacements.append((env['end_coords'], env_end))
    return replacements

def apply_replacements(text: str, replacements, DEBUG = False) -> str:
    """
    replacements here is a list of tuples ((start, end), replacement)
    indicating that the text fragment text[start:end] should be cut out and replaced by
    the `replacement` string.

    I had to write this logic at least four times in this project
    until I realized that I should extract it into a separate function and unify all slightly
    different approaches to this task.
    """
    replacements.sort(key = lambda t: t[0][0])
    new_text = ''
    processed_up_to = 0
    for (start, end), value in replacements:
        if start > processed_up_to:
            new_text += text[processed_up_to:start]
        new_text += value
        processed_up_to = end
        if DEBUG:
            # printing out the coordinates start:end was invaluable in debugging logic
            # mistakes like using `end-start` instead of `end` in the tuple.
            logger.debug(f"Replaced text fragment ({start}:{end}) {text[start:end]} by {value}")
    if processed_up_to < len(text):
        new_text += text[processed_up_to:]
    return new_text

def convert_environments(text: str):
    r'''
    Processes typst "environments" into their LaTeX equivalents. See `find_typst_environments` for details.
    '''
    environments = find_typst_environments(text)
    replacements = []
    for env in environments:
        replacements += handle_environment(text, env)
    return apply_replacements(text, replacements)

def convert_text_markup(text: str, math_mode_mask: list[bool]):
    """
    convert_text_markup locates markdown-like formatting in typst source 
    and replaces it with the TeX-style \textbf{} and \textit{}.
    """
    markup = [('_', '_', r'\textit{', r'}'),
              ('*', '*', r'\textbf{', r'}')]
    replacements = []
    def is_commented_out(text: str, pos):
        line_start = text.rfind('\n', 0, pos)
        if line_start == -1:
            return False
        if re.match(r'^( *)%', text[line_start+1:pos]):
            return True
        return False
    def find_next_notmath(text: str, math_mode_mask, s, start):
        pos = text.find(s, start)
        while pos != -1 and (math_mode_mask[pos] or is_commented_out(text, pos)):
            pos = text.find(s, pos+1)
        return pos
    def find_next_notmath_begin(text: str, math_mode_mask, s, start):
        pos = find_next_notmath(text, math_mode_mask, s, start)
        while pos != -1 and (pos > 0 and text[pos-1].isalnum()):
            pos = find_next_notmath(text, math_mode_mask, s, pos+1)
        return pos
    def find_next_notmath_end(text: str, math_mode_mask, s, start):
        pos = find_next_notmath(text, math_mode_mask, s, start)
        while pos != -1 and (pos < len(text)-1 and text[pos+1].isalnum()):
            pos = find_next_notmath(text, math_mode_mask, s, pos+1)
        return pos
    for m in markup:
        pos = 0
        m_begin, m_end, r_begin, r_end = m
        pos = find_next_notmath_begin(text, math_mode_mask, m_begin, pos)
        while pos != -1:
            endpos = find_next_notmath_end(text, math_mode_mask, m_end, pos+1)
            if endpos == -1:
                logger.debug(f"Could not find proper ending for markup around the following text: {text[pos-100:pos+100]}")
            assert(endpos != -1) # assume well-formed mark-up
            replacements.append(((pos, pos + len(m_begin)), r_begin))
            replacements.append(((endpos, endpos + len(m_end)), r_end))
            pos = find_next_notmath_begin(text, math_mode_mask, m_begin, endpos+1)
    return apply_replacements(text, replacements)

def convert_typst_comments(text: str):
    new_text = re.sub(r'^(\s*)//', r'\1%', text, flags=re.MULTILINE)
    return new_text

def convert_typst_lists(text: str, math_mode_mask: list[bool]):
    replacements = []
    pos = 0
    while True:
        list_start = re.search(r'^( *)\- ', text[pos:], flags=re.MULTILINE)
        if not list_start:
            break
        # logger.debug(f"Found list_start at {list_start.span()[0] + pos}: near {text[pos + list_start.span()[0]-20:pos + list_start.span()[1]+20]}")
        if math_mode_mask[pos + list_start.span()[0]]:
            # not a real list, just a line starting with a minus sign in math mode
            pos = list_start.span()[1]
            continue
        indent = len(list_start.groups()[0])
        list_first_line_starts = pos + list_start.span()[0]
        list_end = re.search('^' + (' {0,' + str(indent) + '}') + r'[^ \-]', text[list_first_line_starts:], flags=re.MULTILINE)
        list_last_line_ends = len(text) if list_end is None else list_first_line_starts + list_end.span()[0]
        pos = list_last_line_ends
        replacements.append(((list_first_line_starts, list_first_line_starts), (' ' * indent) + '\\begin{itemize}\n'))
        for m in re.finditer(r'^' + (' ' * indent) + '-', text[list_first_line_starts:list_last_line_ends], flags=re.MULTILINE):
            hyphen_pos = list_first_line_starts + m.span()[1] - 1
            replacements.append(((hyphen_pos, hyphen_pos+1), '\\item'))
        replacements.append(((list_last_line_ends, list_last_line_ends), (' ' * indent) + '\\end{itemize}\n'))
    # Numbered lists are processed in exactly the same way.
    pos = 0
    while True:
        list_start = re.search(r'^( *)\+ ', text[pos:], flags=re.MULTILINE)
        if not list_start:
            break
        # logger.debug(f"Found numbered list starting at {list_start.span()[0] + pos}, near {text[pos + list_start.span()[0]-20:pos + list_start.span()[1]+20]}")
        if math_mode_mask[pos + list_start.span()[0]]:
            pos = list_start.span()[1]
            continue
        indent = len(list_start.groups()[0])
        list_first_line_starts = pos + list_start.span()[0]
        list_end = re.search('^' + (' {0,' + str(indent) + '}') + r'[^ \+]', text[list_first_line_starts:], flags=re.MULTILINE)
        list_last_line_ends = len(text) if list_end is None else list_first_line_starts + list_end.span()[0]
        pos = list_last_line_ends
        replacements.append(((list_first_line_starts, list_first_line_starts), (' ' * indent) + '\\begin{enumerate}\n'))
        for m in re.finditer(r'^' + (' ' * indent) + '\+', text[list_first_line_starts:list_last_line_ends], flags=re.MULTILINE):
            hyphen_pos = list_first_line_starts + m.span()[1] - 1
            replacements.append(((hyphen_pos, hyphen_pos+1), '\\item'))
        replacements.append(((list_last_line_ends, list_last_line_ends), (' ' * indent) + '\\end{enumerate}\n'))
    return apply_replacements(text, replacements)

def numbered_eq_hack_convert(text: str, math_mode_mask: list[bool]):
    r"""
    Given a typst fragment of the form
      #numbered_eq[
        $ some equation here $
      ] <eq:label>
    this function changes the position of the label to look like
      % #numbered_eq[
        $ some equation here $ <eq:label>
      % ]
    This step simplifies the processing of the display math significantly when we assume
    that typst source defines and uses `numbered_eq` environment as above. This transformation
    is applied only when --numbered-eq-hack command line argument is provided.
    """
    replacements = []
    for match in re.finditer(r'#numbered_eq', text):
        bracket_opens = match.span()[1]
        assert(text[bracket_opens] == '[')
        bracket_closes = find_closing_bracket(text, bracket_opens)
        if text[bracket_closes+1:bracket_closes+3] == ' <':
            label_starts = bracket_closes + 3
            label_ends = text.find('>', label_starts)
            if label_ends == -1:
                raise ValueError(f"Couldn't parse label after a #numbered_eq environment: {text[match.span()[0]:min(len(text), label_starts + 30)]}")
            label = text[label_starts:label_ends]
            closing_dollar = text.rfind('$', bracket_opens, bracket_closes)
            assert(closing_dollar != -1)
            replacements.append(((label_starts-1, label_ends+1), ' '))
            replacements.append(((closing_dollar, closing_dollar+1), '$ <' + label + '>'))
            # comment out the numbered_eq environment
            environment_start, _ = match.span()
            replacements.append(((environment_start, environment_start+1), '% #'))
            replacements.append(((bracket_closes, bracket_closes+1), '% ]'))
    return apply_replacements(text, replacements)

def convert_typst_display_math(text: str, math_mode_mask: list[bool]):
    replacements = []
    pos = 0
    while pos < len(text):
        match = re.search(r'^( *)\$\s', text[pos:], re.MULTILINE)
        if not match:
            break
        match_start, match_end = match.span()
        start = match_start + pos
        end = match_end + pos
        indentation = match.groups()[0]
        mode_enter_start = start + len(indentation)
        mode_enter_end = mode_enter_start + 2
        closing_dollar = text.find('$', end)
        assert(closing_dollar != -1)
        if not text[closing_dollar-1].isspace():
            raise ValueError(f"Invalid typst display math sequence: {text[match_start:min(len(text), closing_dollar+10)]}")
        mode_leave_start = closing_dollar-1
        mode_leave_end = mode_leave_start + 2

        alignment_needed = False
        if text.find('&', start, closing_dollar) != -1:
            alignment_needed = True
        label = None
        _, symbol_after_dollar = whitespace_around_character(text, closing_dollar)
        if symbol_after_dollar < len(text) and text[symbol_after_dollar] == '<':
            label_start = symbol_after_dollar + 1
            label_end = label_start
            while label_end < len(text) and (text[label_end].isalnum() or (text[label_end] in ['-', '_', ':'])):
                label_end += 1
            assert(text[label_end] == '>')
            label = text[label_start:label_end]
            mode_leave_end = label_end + 1
        
        if label is None:
            tex_mode_enter = r'\['
            if alignment_needed:
                tex_mode_enter = r'\[ \begin{aligned}'
            tex_mode_leave = r'\]'
            if alignment_needed:
                tex_mode_leave = r'\end{aligned} \]'
            mode_enter_end -= 1
            mode_leave_start += 1
            replacements.append(((mode_enter_start, mode_enter_end), tex_mode_enter))
            replacements.append(((mode_leave_start, mode_leave_end), tex_mode_leave))
        else:
            tex_mode_enter = r'\begin{equation}' + '\n' + indentation + r'  \label{' + label + '}\n' + indentation + '  '
            if alignment_needed:
                tex_mode_enter += r'\begin{aligned}' + '\n' + indentation + '  '
            # Strictly speaking if the equation takes multiple lines in typst code, we may need to
            # correct the indentation of all the following lines, but that's quite annoying.
            tex_mode_leave = r'\end{equation}'
            if alignment_needed:
                tex_mode_leave = r'  \end{aligned}' + '\n' + indentation + tex_mode_leave
            if text[closing_dollar-1] != '\n':
                tex_mode_leave = '\n' + indentation + tex_mode_leave
            replacements.append(((mode_enter_start, mode_enter_end), tex_mode_enter))
            replacements.append(((mode_leave_start, mode_leave_end), tex_mode_leave))
        pos = closing_dollar + 1
    return apply_replacements(text, replacements)

def convert_typst_fake_quotients(text: str, math_mode_mask: list[bool]):
    r"""
    typst uses a bizarre convention that a single slash in math mode is converted into what's written as \frac{}{}
    in TeX. This is something I almost never want, so every time I write a quotient object I have to escape the
    slash symbol.
    """
    replacements = []
    for quot_match in re.finditer(r'\\/', text):
        start, end = quot_match.span()
        if not math_mode_mask[start]:
            continue
        replacements.append(((start, start+2), '/'))
    return apply_replacements(text, replacements)

def convert_typst_linebreaks(text: str, math_mode_mask: list[bool]):
    r"""
    Replaces typst-like linebreaks (backslash, endline) with tex-like (double backslash).
    Also handles `#linebreak` commands.
    """
    replacements = []
    for match in re.finditer(r'\\\n', text, re.MULTILINE):
        start, end = match.span()
        if not math_mode_mask[start]:
            continue
        # Avoid double-converting TeX-style backslashes (can happen, for example, after converting a typst-style matrix)
        if start > 0 and text[start-1] == '\\':
            continue
        replacements.append(((start, start + 1), '\\\\'))
    for match in re.finditer(r'#linebreak\(\)(\s)', text, re.MULTILINE):
        start, end = match.span()
        replacements.append(((start, end), r'\\' + match.groups()[0]))
    return apply_replacements(text, replacements)

def make_brackets_visible(text: str, math_mode_mask: list[bool]):
    r"""
    Replaces brackets { } in typst math mode with \{ \} for LaTeX
    """
    replacements = []
    for match in re.finditer(r'[{}]', text):
        start, end = match.span()
        if not math_mode_mask[start]:
            continue
        replacements.append(((start, start + 1), '\\' + text[start]))
    return apply_replacements(text, replacements)

def convert_colon_spacing(text: str, math_mode_mask: list[bool]):
    r"""
    Replaces colons ':' in typst math mode with \colon for LaTeX if preceded by a non-space character.
    """
    replacements = []
    for match in re.finditer(r'(?<=\S): ', text):
        start, end = match.span()
        if not math_mode_mask[start]:
            continue
        replacements.append(((start, start + 2), r'\colon '))
    return apply_replacements(text, replacements)

def replace_magic_arrows(text: str, math_mode_mask: list[bool]):
    r"""
    Replaces `->` and '<-' in typst math mode with LaTeX \to arrows. Handles supscripts
    by using \xrightarrow or \xleftarrow.
    """
    replacements = []
    arrows = [('->', r'\to', r'\xrightarrow'), ('<-', r'\leftarrow', r'\xleftarrow')]
    for arrow, tex_basic_arrow, tex_arrow in arrows:
        for match in re.finditer(arrow, text):
            start, arrow_end = match.span()
            if not math_mode_mask[start]:
                continue
            end = arrow_end
            if text[arrow_end] == ' ' or text[arrow_end] == '\n':
                replacements.append(((start, end), tex_basic_arrow))
            elif text[arrow_end] == '^':
                if text[arrow_end+1] == '(':
                    closing_bracket = find_closing_bracket(text, arrow_end+1, single_line_mode=True)
                    end = closing_bracket+1
                    replacements.append(((start, arrow_end+2), tex_arrow + '{'))
                    replacements.append(((closing_bracket, closing_bracket+1), '}'))
                else:
                    # simple supscript with no parentheses, like `A ->^f B`
                    # Note that we don't follow typst convention in parsing $->^f(x, y)$ as having `f(x, y)` as a supscript
                    # since LaTeX doesn't do that and inserting extra parentheses could be annoying
                    i = arrow_end+1
                    while text[i].isalnum():
                        i += 1
                    end = i
                    replacements.append(((start, arrow_end+1), tex_arrow + '{'))
                    replacements.append(((end, end), '}'))
    return apply_replacements(text, replacements)

class TestConversionE2E(unittest.TestCase):
    def test_showcase(self):
        typst_code = r'''= Section name <sec:section_label>

Here is a *very important* result:

#theorem[
  The following two objects are both zero:
  - $binom(4, 2) dot 3 - dim(ker(CC^(18) ->^("zero") CC))$;
  - $mat(1, 0; 0, 1) - mat(1, cal(F) \/ cal(F); 0, 1)$
] <thm:main_theorem>

To prove theorem~@thm:main_theorem we need the vanishing of
$ QQ times.circle ZZ \/ n ZZ = 0, $ <eq:torsion_and_divisible>
which we discussed last time. Recall the morphism
$ f: x arrow.bar 2x $
used above.'''
        expected_output = r'''\section{Section name}
\label{sec:section_label}

Here is a \textbf{very important} result:

\begin{theorem}
  \label{thm:main_theorem}
  The following two objects are both zero:
  \begin{itemize}
  \item $\binom{4}{2} \cdot 3 - \dim(\ker(\CC^{18} \xrightarrow{\mathrm{zero}} \CC))$;
  \item $\left(\begin{matrix} 1 & 0 \\ 0 & 1 \end{matrix}\right) - \left(\begin{matrix} 1 & \mathcal{F} / \mathcal{F} \\ 0 & 1 \end{matrix}\right)$
  \end{itemize}
\end{theorem}

To prove theorem~\ref{thm:main_theorem} we need the vanishing of
\begin{equation}
  \label{eq:torsion_and_divisible}
  \QQ \otimes \ZZ / n \ZZ = 0,
\end{equation}
which we discussed last time. Recall the morphism
\[ f\colon x \mapsto 2x \]
used above.'''
        self.assertEqual(expected_output, convert_text(typst_code))

def convert_text(text, bib_refs: list[str] = [], numbered_eq_hack=False) -> str:
    math_commands = read_math_commands()
    new_text = text

    bibliography = re.search(r'#bibliography\("(.+)"\)', text)
    if bibliography:
        bib_file_name = bibliography.groups()[0]
        try:
            bibtext = open(bib_file_name, 'r').read()
            bib_refs += parse_bibliography(bibtext)
        except:
            pass

    new_text = convert_typst_comments(new_text)
    math_mode_mask = parse_math_mode_mask(new_text)
    if numbered_eq_hack:
        new_text = numbered_eq_hack_convert(new_text, math_mode_mask)
        math_mode_mask = parse_math_mode_mask(new_text)

    new_text = make_brackets_visible(new_text, math_mode_mask)
    # Embedded lists are handled by iterating the conversion several times.
    for _ in range(3):
        math_mode_mask = parse_math_mode_mask(new_text)
        processed_lists = convert_typst_lists(new_text, math_mode_mask)
        if processed_lists == new_text:
            break
        new_text = processed_lists

    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_underline(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = replace_magic_arrows(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = math_rebrace_sub_sup(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = math_slashify(new_text, math_mode_mask, math_commands)

    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_sections(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_environments(new_text)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_text_markup(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = refs_texify(new_text, bib_refs=bib_refs)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = math_quoted_text_mathrm(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_typst_fake_quotients(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_colon_spacing(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_typst_linebreaks(new_text, math_mode_mask)
    math_mode_mask = parse_math_mode_mask(new_text)
    new_text = convert_typst_display_math(new_text, math_mode_mask)
    return new_text

def main():
    parser = argparse.ArgumentParser(description="Convert typst syntax to LaTeX syntax.")
    parser.add_argument('input', type=str, help='The typst source file. Use "-" to read from stdin.')
    parser.add_argument('output', type=str, nargs='?', default='-', help='The file to write LaTeX code. Defaults to "-", the stdout.')
    
    parser.add_argument('--bibliography', type=str, help=r'Bibliography file to choose between \ref and \cite for LaTeX.')
    parser.add_argument('--prelude', type=str, help='Prepend the contents of the specified file to the converted text.')
    parser.add_argument('--skip-to-contents', action='store_true', help='Start conversion with the first non-indented line that does not start with # or )')

    parser.add_argument('--numbered-eq-hack', action='store_true', help='(not intended for general usage, see the numbered_eq_hack_convert function)')

    args = parser.parse_args()
    
    typst_source = ''
    if args.input == '-':
        typst_source = sys.stdin.read()
    else:
        try:
            typst_source = open(args.input, 'r').read()
        except:
            logger.error(f"Could not read input file {args.input}")
            exit(1)
    if args.skip_to_contents:
        contents_line = re.search(r'^[^\s#\)/]', typst_source, re.MULTILINE)
        if contents_line is not None:
            typst_source = typst_source[contents_line.span()[0]:]
    # workaround to simplify some patterns related to line breaks
    typst_source = '\n' + typst_source
    bib_refs = []
    if args.bibliography:
        try:
            bibtext = open(args.bibliography, 'r').read()
            bib_refs = parse_bibliography(bibtext)
        except:
            logger.error(f"Could not read bibliography file {args.bibliography}")
            exit(1)
    output = ''
    if args.prelude:
        try:
            prelude_text = open(args.prelude, 'r').read()
            output += prelude_text
        except:
            logger.error(f"Could not read prelude file {args.prelude}")
            exit(1)
    # NB: skip an extra '\n' added as a workaround above
    output += convert_text(typst_source, bib_refs=bib_refs, numbered_eq_hack=args.numbered_eq_hack)[1:]

    if args.output == '-':
        print(output, end = None)
    else:
        open(args.output, 'w').write(output)


if __name__ == "__main__":
    main()
