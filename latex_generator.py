"""
LaTeX Template Generator Module
Handles LaTeX template creation and management
"""

import subprocess
import platform
from pathlib import Path
from typing import Optional, Tuple


class LaTeXGenerator:
    """Manages LaTeX templates and generates base template structure"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize LaTeX generator
        
        Args:
            template_dir: Directory containing LaTeX templates (optional)
        """
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = Path(__file__).parent / "templates"
        
        self.template_dir.mkdir(exist_ok=True)
    
    def get_default_template(self) -> str:
        """
        Get default LaTeX resume template structure
        
        Returns:
            LaTeX template string
        """
        return r"""
        %-------------------------------------------
% Resume in LuaLatex
% Author: Kumar Pallav
% (Works with Overleaf)
%-------------------------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage[urw-garamond]{mathdesign}
\RequirePackage{luatex85}
\usepackage{pdfcomment}
\usepackage{luacode}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
%-------------------------------------------
\addtolength{\oddsidemargin}{-0.475in}
\addtolength{\evensidemargin}{-0.375in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
%-------------------------------------------
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Custom commands
%-------------------------------------------
\newcommand{\resumeItem}[2]{
  \item{
    \textbf{#1}{: \small #2 \vspace{-2pt}}
  }
}

\newcommand{\resumeEduEntry}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{#3} & \textit{#4} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeExpEntry}[5]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{#3 $\cdot$ #4} & \textit{#5} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-4pt}}

\renewcommand{\labelitemii}{$\circ$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*,label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\setlist{rightmargin=10pt}\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

% Load lua script
%-------------------------------------------
\begin{luacode}
require("lua/parser.lua")
\end{luacode}

% Print Heading
%-------------------------------------------
\directlua{printHeading("_data/personal.json")}

% Print Education
%-------------------------------------------
\section{Education}
  \resumeSubHeadingListStart
	\directlua{printEduItems("_data/edu.json")}
  \resumeSubHeadingListEnd

% Print Experience
%-------------------------------------------
\section{Experience}
  \resumeSubHeadingListStart
  	\directlua{printExpItems("_data/exp.json")}
  \resumeSubHeadingListEnd

% Print Projects
%-------------------------------------------
\section{\href{https://github.com/pforpallav}{Projects}}
  \resumeSubHeadingListStart
    \directlua{printProjItems("_data/proj.json")}
  \resumeSubHeadingListEnd
  
% Print Skills
%-------------------------------------------
\section{Programming Skills}
  \resumeSubHeadingListStart 
    \item{
      \textbf{Languages}{: \directlua{printList("_data/personal.json", "languages", "language")}}
      \hfill
      \textbf{Technologies}{: \directlua{printList("_data/personal.json", "technologies", "technology")}}
      }
  \resumeSubHeadingListEnd

\end{document}
        """
    
    def load_template(self, template_name: str) -> str:
        """
        Load a LaTeX template from file
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Template content as string
        """
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_template(self, template_name: str, content: str):
        """
        Save a LaTeX template to file
        
        Args:
            template_name: Name of the template file
            content: Template content
        """
        template_path = self.template_dir / template_name
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def save_latex_output(self, latex_content: str, output_path: str):
        """
        Save final LaTeX document to file
        
        Args:
            latex_content: Complete LaTeX document
            output_path: Path to save the .tex file
            
        Returns:
            Path to saved .tex file
        """
        output_path = Path(output_path)
        
        # Ensure .tex extension
        if output_path.suffix != '.tex':
            output_path = output_path.with_suffix('.tex')
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        return output_path
    
    def compile_to_pdf(self, tex_path: str, cleanup: bool = True) -> Tuple[bool, Optional[Path]]:
        """
        Compile LaTeX file to PDF using pdflatex
        
        Args:
            tex_path: Path to the .tex file
            cleanup: Whether to delete intermediate files (.log, .aux, etc.)
            
        Returns:
            Tuple of (success: bool, pdf_path: Optional[Path])
            
        Reference: https://coderslegacy.com/converting-latex-to-pdf-in-python/
        """
        tex_path = Path(tex_path)
        
        if not tex_path.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_path}")
        
        if tex_path.suffix != '.tex':
            raise ValueError(f"File must have .tex extension: {tex_path}")
        
        # Get the directory and filename without extension
        work_dir = tex_path.parent
        tex_filename = tex_path.name
        
        # Check if pdflatex is available
        try:
            # Test if pdflatex is in PATH
            result = subprocess.run(
                ["pdflatex", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "pdflatex not found. Please install a LaTeX distribution:\n"
                "  - Windows: Install MiKTeX (https://miktex.org/)\n"
                "  - Linux: sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-extra\n"
                "  - macOS: Install MacTeX or use: brew install --cask mactex"
            )
        
        # Determine shell parameter based on OS
        shell_param = platform.system() == "Windows"
        
        try:
            # Run pdflatex (may need to run twice for references/cross-references)
            print(f"   Compiling LaTeX to PDF (this may take a moment)...")
            
            # First compilation
            result1 = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_filename],
                cwd=work_dir,
                shell=shell_param,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Second compilation (for proper cross-references, table of contents, etc.)
            result2 = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_filename],
                cwd=work_dir,
                shell=shell_param,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Check if PDF was created
            pdf_path = work_dir / f"{tex_path.stem}.pdf"
            
            if pdf_path.exists():
                # Cleanup intermediate files if requested
                if cleanup:
                    self._cleanup_intermediate_files(tex_path)
                
                return True, pdf_path
            else:
                # PDF not created, show error
                error_msg = result2.stderr or result2.stdout
                print(f"   ⚠️  Warning: PDF compilation may have issues. Check LaTeX output.")
                return False, None
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("PDF compilation timed out. The LaTeX file may be too complex.")
        except Exception as e:
            raise RuntimeError(f"Error during PDF compilation: {str(e)}")
    
    def _cleanup_intermediate_files(self, tex_path: Path):
        """
        Delete intermediate LaTeX compilation files
        
        Args:
            tex_path: Path to the .tex file
        """
        work_dir = tex_path.parent
        base_name = tex_path.stem
        
        # List of intermediate file extensions to delete
        intermediate_extensions = ['.log', '.aux', '.out', '.synctex.gz', '.fdb_latexmk', '.fls']
        
        for ext in intermediate_extensions:
            intermediate_file = work_dir / f"{base_name}{ext}"
            if intermediate_file.exists():
                try:
                    intermediate_file.unlink()
                except Exception:
                    pass  # Ignore errors during cleanup

