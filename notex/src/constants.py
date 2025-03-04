latex_preamble_str = r"""
\documentclass{article}
\usepackage[headheight=20pt, margin=1.0in, top=1.2in]{geometry}
\usepackage{amsmath, amssymb, amsthm, thmtools, tcolorbox, array, graphicx, makeidx, cancel, multirow, fancyhdr, xypic, color, nicefrac, rotating, multicol, caption, subcaption, xcolor, tikz, tikz-3dplot, tikz-cd, pgfplots, import, enumitem, calc, booktabs, wrapfig, siunitx, hyperref,float}
\hypersetup{colorlinks=true,linkcolor=blue}
\usepackage[all]{xy}
\usepackage{esint}
\setlength{\parindent}{0in}
\sisetup{per-mode = symbol}
\usetikzlibrary{calc,arrows,svg.path,decorations.markings,patterns,matrix,3d,fit}
\usepgfplotslibrary{groupplots}
\pgfplotsset{compat=newest}
\newtcolorbox{mydefbox}[2][]{colback=red!5!white,colframe=red!75!black,fonttitle=\bfseries,title=#2,#1}
\newtcolorbox{mythmbox}[2][]{colback=gray!5!white,colframe=gray!75!black,fonttitle=\bfseries,title=#2,#1}
\newtcolorbox{myexamplebox}[2][]{colback=green!5!white,colframe=green!75!black,fonttitle=\bfseries,title=#2,#1}
\newtcolorbox{mypropbox}[2][]{colback=blue!5!white,colframe=blue!75!black,fonttitle=\bfseries,title=#2,#1}
\declaretheoremstyle[headfont=\color{blue}\normalfont\bfseries,]{colored}
\theoremstyle{definition}
\newtheorem{theorem}{Theorem}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{problem}[theorem]{Problem}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{exercise}[theorem]{Exercise}
\newtheorem{example}[theorem]{Example}
\newtheorem{solution}[theorem]{Solution}
\newtheorem*{thm}{Theorem}
\newtheorem*{lem}{Lemma}
\newtheorem*{prob}{Problem}
\newtheorem*{exer}{Exercise}
\newtheorem*{prop}{Proposition}
\def\R{\mathbb{R}}
\def\F{\mathbb{F}}
\def\Q{\mathbb{Q}}
\def\C{\mathbb{C}}
\def\N{\mathbb{N}}
\def\Z{\mathbb{Z}}
\def\Ra{\Rightarrow}
\def\e{\epsilon}
\newcommand{\typo}[1]{{\color{red}{#1}}}
\newcommand\thedate{\today}
\newcommand{\mb}{\textbf}
\newcommand{\norm}[2]{\|{#1}\|_{#2}}
\newcommand{\normm}[1]{\|#1\|}
\newcommand{\mat}[1]{\begin{bmatrix} #1 \end{bmatrix}}
\newcommand{\eqtext}[1]{\hspace{3mm} \text{#1} \hspace{3mm}}
\newcommand{\set}[1]{\{#1\}}
\newcommand{\inte}{\textrm{int}}
\newcommand{\ra}{\rightarrow}
\newcommand{\minv}{^{-1}}
\newcommand{\tx}[1]{\text{ {#1} }}
\newcommand{\abs}[1]{|#1|}
\newcommand{\mc}[1]{\mathcal{#1}}
\newcommand{\uniflim}{\mathop{\mathrm{unif\lim}}}
\newcommand{\notimplies}{\mathrel{{\ooalign{\hidewidth$\not\phantom{=}$\hidewidth\cr$\implies$}}}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Title of the Document}
\fancyhead[C]{}
\fancyhead[R]{\thepage}
\fancyfoot[L]{}
\fancyfoot[C]{}
\fancyfoot[R]{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\numberwithin{equation}{section}
% Increase spacing between paragraphs
\setlength{\parskip}{1em}
% Increase spacing before and after sections
\usepackage{titlesec}
\titlespacing*{\section}{0pt}{3ex plus 1ex minus .2ex}{2ex plus .2ex}
\titlespacing*{\subsection}{0pt}{2ex plus 1ex minus .2ex}{1ex plus .2ex}
\titlespacing*{\subsubsection}{0pt}{1ex plus 1ex minus .2ex}{1ex plus .2ex}
\title{\textbf{Title of the Document}}
\author{Author Name}
\date{\today}
\begin{document}
\maketitle
\tableofcontents
\newpage
"""

latex_issues_prompt = r"""
- Duplicate \usepackage[all]{xy}: The package xy is loaded twice, once within the main \usepackage line and again separately.
- Usage of \begin{align} in Non-Math Environments: Using \begin{align} inside figure captions and text is incorrect. This should be plain text or wrapped in $...$ for inline math.
- Improper Math Mode Usage in Text: In figure labels and captions, such as \begin{align} x \end{align} should be $x$.
- Misplaced Commands: Commands like \mathbb{R} and \Rightarrow should be used within math mode.
- Incomplete Definitions: The definitions of \mathbb{B}_r and similar symbols are used without being wrapped in math mode $.
- Overuse of \begin{align}: There is an overuse of the align environment for simple inline math that should use $...$.
- Improper Usage of \begin{figure}[h] and [h] vs. [H]: [h] should be used instead of [H] for figure placement to avoid potential issues with the float package.
- Improper Nesting of Environments: Make sure \begin{enumerate} and other environments are correctly nested and closed.
- Unnecessary Bold in Theorems and Definitions: The use of \textbf{Definition 2.1} within the \begin{definition}...\end{definition} environment is redundant.
- Use of \qed Instead of Closing Proof Environment: Ensure that all proofs are properly opened with \begin{proof} and closed with \end{proof} rather than using \qed.
- Misplaced \tableofcontents: It’s placed after \maketitle, which is correct, but might need to adjust to ensure proper page numbering.
- Redundant Loading of TikZ Libraries: Libraries calc and tikz-cd are loaded twice.
- Misuse of \def vs. \newcommand: \def is used instead of \newcommand which is more appropriate for user-defined commands.
- Unused Imports: Ensure all imported packages are necessary.
- No New Line for \section: Ensure proper spacing and new lines before \section and \subsection commands.
- Math Mode in Section Titles: Section titles containing math, such as \section{The Topology of \mathbb{R}^n}, should ensure proper math mode within titles.
- Undefined Control Sequences: Ensure all used commands and symbols are defined or included within the appropriate package.
- Caption Outside Float Environment: Ensure \caption is used within a proper float environment such as figure.
- Potential Overlapping and Incorrect Spacing: Use of \titlespacing* might need adjustments to ensure no overlapping or awkward spacing in the document.
- Avoid: Extra }, or forgotten \endgroup.
- Avoid: Missing number, treated as zero.
- You can't use `\raise' in vertical mode.
- Avoid: Illegal unit of measure (pt inserted).
- Avoid: Runaway argument?
- Avoid: Argument of \xP@rotate@ has an extra }
- Avoid: Illegal parameter number in definition of \Hy@tempa.
- Avoid: Extra \endgroup.
- Avoid: Too many }'s.
- Avoid: Extra \endgroup.
- Avoid: Package caption Error: \caption outside float.
- Avoid: LaTeX Error: \begin{document} ended by \end{tikzpicture}.
- Avoid: Undefined control sequence.
DO NOT INSERT ALIGN INTO FIGURES.
"""

preamble_instructions = (
    r"You are a LaTeX converter. Do not output anything other than the LaTeX code. Ensure the script is valid and has no errors. "
    r"Make sure the LaTeX you write is perfect and has no errors. Ensure things are in math-mode when they need to be. "
    r"Ensure all commands are finished and have an end. Recognize sections, theorems, proofs, questions, exercises, problems, solutions, "
    r"DO NOT USE ALIGN IN FIGURES"
    r"BOLD AND UNDERLINE IN RED ANYTHING YOYU ARE UNSURE OF."
    r"and diagrams and format them properly. Maintain the continuity of the document. Use appropriate LaTeX commands for theorems, definitions, "
    r"proofs, exercises, examples, and solutions. Use environments such as \\begin{theorem}...\\end{theorem}, \\begin{definition}...\\end{definition}, "
    r"\\begin{proof}...\\end{proof}. Use \\section{...}, \\subsection{...}, and \\subsubsection{...} to organize the document into clearly defined sections. "
    r"Ensure proper spacing between different elements and avoid redundant commands. For diagrams and photographs, describe the content briefly in LaTeX comments. "
    r"If photographs or images of text are unclear, make reasonable guesses but note these as comments. Do not include \\documentclass, \\usepackage, \\begin{document}, or \\end{document} commands in your response. "
    r"Unescaped Special Characters: Some special characters like underscores (_) and ampersands (&) need to be escaped in LaTeX. "
    r"Math Mode Delimiters: Ensure that math mode delimiters ($ or \\[...\\]) are used appropriately. "
    r"Incomplete Environments: Make sure all environments are properly opened and closed. "
    r"Overlapping Definitions: Ensure definitions are not overlapping and properly formatted. "
    r"Remove Extra Symbols and Comments: Ensure there are no residual symbols or comments that could cause LaTeX errors. "
    r"Try to link examples and proofs together. "
    r"Abstain from undefined control sequences. "
    r"When giving a definition, theorem, proposition or anything of that nature, enclose in \\textbf{...} the name of it, followed by descriptions. "
    r"Any solutions or proofs should be started with \\begin{proof} and obviously closed by \\end{proof}. "
    r"Use \\frac when discussing a fraction. "
    r"Do not use solutions unless it's clearly a problem set, use proof instead. "
    r"Use sections, subsections, newpage, subsubsection intelligently and discern how information should be organized. "
    r"Ensure all environments are properly closed: Make sure each \\begin{...} has a corresponding \\end{...}. "
    r"Ensure that there is no overflow horizontally. Do not use \\textbf{...} for unnecessary emphasis, focus on clarity and conciseness. "
    r"For figures, use the tikz package to create diagrams rather than referencing non-existent PNG files. Ensure that figures are fully defined and correct. For example, use \\begin{tikzpicture}...\\end{tikzpicture} to create figures. "
    r"Use \\begin{figure}[h]...\\end{figure} to include figures with captions, ensuring that each figure environment is properly closed and includes a caption. "
    r"Ensure the LaTeX document compiles without errors by carefully closing all open environments and properly formatting the document. "
    r"Do not generate non-existent file references or incomplete LaTeX code. Ensure all figures and images are created using LaTeX code. "
    r"If you encounter complex diagrams or graphs, use the tikz package to replicate them within LaTeX as accurately as possible. "
    r"If you need to create graphs or plots, use the pgfplots package to ensure they are generated within LaTeX. "
    r"Figure Placement: Use `[h]` instead of `[H]` for figure placement to allow flexibility in positioning and avoid formatting issues."
    r"Proper Use of `align` Environment: Ensure that only mathematical expressions are wrapped within `align`. Do not use `align` for non-mathematical content."
    r"Proof Environment: Use `\\begin{proof}` and `\\end{proof}` for proofs instead of `\\qed`."
    r"Math Mode Delimiters: Ensure that math mode delimiters (`$` or `\\[...\\]`) are used appropriately around mathematical content."
)

latex_end_str = r"\end{document}"


GPT_COST = {"input_token_cost": 5.0, "output_token_cost": 15.0}
