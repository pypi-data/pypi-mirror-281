# typsytex

`typsytex` is a tool that converts typst markup to an equivalent LaTeX code. It's intended for
smallish text fragments and **only handles syntax**, no scripting or command definitions.

Typst is a document typesetting system, an attempt to create a new generation LaTeX.
One of its features is a much less noisy syntax.
`typsytex` is a tool that replaces all syntax sugar 
from typst-formatted documents by their LaTeX equivalents.

This is a very dumb tool, a bunch of regular expressions with some glue code. It only
works for properly indented documents with no unbalanced brackets. 
It's very easy to write a valid typst document that will be converted to a broken
LaTeX code if you try.

## Usage

### Install
Locally: just download the `typsytex.py` file from this repository and make it executable.

Globally: run `pip3 install typsytex`, then use `typsytex` command.

### Converting files
Run `typsytex typst_source.typ latex_output.tex` to convert the
contents of `typst_source.typ` and save the LaTeX code to `latex_output.tex` file. Omitting the output name will output
the code to stdout. For more details, run `typsytex -h`.

## Showcase

Converts this:
```typst
= Section name <sec:section_label>

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
used above.
```

To this:
```LaTeX
\section{Section name}
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
used above.
```

## Supported features

- **Markdown-style formatting**: the `*bold*` and `_italic_` text is replaced with `\textbf` and `\textit`. Also deals with `= Section` and `== Subsection`, handles labeled (sub)sections.
- **Lists**: typst-style lists (`- first item (line break) - second item (line break)`) are converted to `\begin{itemize}` etc. Only works for correctly indented lists. Also works for the automatically numbered lists (the ones where items start with `+`, not markdown-style with numbers).
- **Environments**: converts fragments like 
```
#theorem[
  Contents
] <thm:main_theorem>
```
to LaTeX-style
```
\begin{theorem}
  \label{thm:main_theorem}
  Contents
\end{theorem}
```
Only works for correctly indented multiline environments. Environments with arguments, like `#theorem(argument)[...]` are kind of supported, but not automatically, you'll need to modify `typsytex` source code to handle them properly.
- **References**: replaces `@thm:main_theorem` with `\ref{thm:main_theorem}`. If a bibliography file is specified in the text or as a command-line argument, switches to `\cite` when necessary.
- **Comments**: converts `// comment` into `% comment`. (Beware: typst code in the commented lines will mostly be translated to LaTeX anyway.)
- **Math mode: display equations**: convert `$ equation $` into `\[ equation  \]`. Handles display equations with labels, detects whether alignment operators are used and converts them accordingly.
- **Math mode: braces for sup/sub**: converts typst-style `x^(n+1)` into `x^{n+1}` expected by LaTeX.
- **Math mode: quoted to mathrm**: converts `x + "something" + y` into `x + \mathrm{something} + y`.
- **Math mode: command translation**: converts functions calling from typst math mode to their LaTeX equivalents: `Psi + binom(3, 2) in union.big U_i` is transformed into `\Psi + \binom{3}{2} \in \bigcup U_i`. Only the commands hardcoded in the source code are translated (in the `MATHCOMMANDS` list).
- **Math mode: magic symbols to commands**: detects the use of things like `->`, `>>` and converts them to `\to`, `\gg`, respectively. Converts `->^(a)` into `\xrightarrow{a}`.

## Unsupported features

The following features are **NOT** supported:
- anything involving scripting, definition of new commands, etc.
- the math mode slash transforming into `\frac` (too difficult to determine the numerator and denumerator properly)
- typst-conforming subscript precedence order: `f_a(1)` in Typst is equivalent to `f_(a(1))` instead of `f_(a)(1)` even when `a` is not a command accepting arguments, unlike LaTeX.



