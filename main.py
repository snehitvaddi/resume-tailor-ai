"""
Resume Updater - Main Application
Orchestrates the resume transformation pipeline
"""

import argparse
import sys
from pathlib import Path
from pdf_extractor import PDFExtractor
from llm_service import LLMService
from latex_generator import LaTeXGenerator


class ResumeUpdater:
    """Main application class for resume transformation"""
    
    def __init__(self, llm_provider: str = "openai", api_key: str = None):
        """
        Initialize Resume Updater
        
        Args:
            llm_provider: "openai" or "gemini"
            api_key: API key for LLM provider
        """
        self.pdf_extractor = PDFExtractor()
        self.llm_service = LLMService(provider=llm_provider, api_key=api_key)
        self.latex_generator = LaTeXGenerator()
    
    def process_resume(self, resume_path: str, job_description: str, output_path: str = "updated_resume.tex", compile_pdf: bool = True):
        """
        Main processing pipeline
        
        Args:
            resume_path: Path to resume (PDF or text file)
            job_description: Job description text
            output_path: Path to save output LaTeX file
            compile_pdf: Whether to automatically compile LaTeX to PDF
            
        Returns:
            Tuple of (latex_path, pdf_path) or (latex_path, None) if compilation skipped/failed
        """
        print("🔄 Starting resume transformation pipeline...")
        print(f"📄 Resume: {resume_path}")
        print(f"💼 Job Description: {len(job_description)} characters")
        print()
        
        # Step 1: Extract text from resume
        print("Step 1/5: Extracting text from resume...")
        resume_path_obj = Path(resume_path)
        
        if resume_path_obj.suffix.lower() == '.pdf':
            resume_text = self.pdf_extractor.extract_text(resume_path)
        else:
            resume_text = self.pdf_extractor.extract_from_text_file(resume_path)
        
        print(f"✅ Extracted {len(resume_text)} characters from resume")
        print()
        
        # Step 2: Transform resume content (Stage 1 LLM call)
        print("Step 2/5: Transforming resume content to match job description...")
        print("   (This may take 30-60 seconds...)")
        transformed_content = self.llm_service.transform_resume_content(resume_text, job_description)
        print(f"✅ Resume content transformed ({len(transformed_content)} characters)")
        print()
        
        # Step 3: Get LaTeX template
        print("Step 3/5: Loading LaTeX template...")
        latex_template = self.latex_generator.get_default_template()
        print("✅ LaTeX template loaded")
        print()
        
        # Step 4: Format to LaTeX (Stage 2 LLM call)
        print("Step 4/5: Formatting content into LaTeX structure...")
        print("   (This may take 30-60 seconds...)")
        final_latex = self.llm_service.format_to_latex(transformed_content, latex_template)
        print("✅ Content formatted into LaTeX")
        print()
        
        # Step 5: Save LaTeX output
        print(f"Step 5/5: Saving LaTeX file to: {output_path}")
        saved_path = self.latex_generator.save_latex_output(final_latex, output_path)
        print(f"✅ LaTeX file saved successfully!")
        print()
        
        pdf_path = None
        
        # Step 6: Compile to PDF (optional)
        if compile_pdf:
            print("📄 Compiling LaTeX to PDF...")
            try:
                success, pdf_path = self.latex_generator.compile_to_pdf(saved_path, cleanup=True)
                if success and pdf_path:
                    print(f"✅ PDF generated successfully!")
                    print(f"📄 PDF file: {pdf_path}")
                else:
                    print(f"⚠️  PDF compilation completed with warnings. Check LaTeX output.")
            except Exception as e:
                print(f"⚠️  PDF compilation failed: {str(e)}")
                print(f"   You can manually compile with: pdflatex {saved_path}")
            print()
        
        # Final summary
        print("=" * 60)
        print("✨ Transformation Complete!")
        print(f"📝 LaTeX file: {saved_path}")
        if pdf_path:
            print(f"📄 PDF file: {pdf_path}")
        else:
            print(f"📄 PDF: Not generated (use --no-pdf to skip, or compile manually)")
        print("=" * 60)
        
        return saved_path, pdf_path


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Transform your resume to match a job description using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using OpenAI (default) - automatically compiles to PDF
  python main.py resume.pdf "Job description text here"
  
  # Using Google Gemini
  python main.py resume.pdf "Job description text here" --provider gemini
  
  # With custom output path
  python main.py resume.pdf "Job description text here" -o custom_resume.tex
  
  # With job description from file
  python main.py resume.pdf -j job_description.txt
  
  # Skip PDF compilation (only generate LaTeX)
  python main.py resume.pdf "Job description" --no-pdf
        """
    )
    
    parser.add_argument(
        "resume",
        type=str,
        help="Path to resume file (PDF or text file)"
    )
    
    parser.add_argument(
        "job_description",
        type=str,
        nargs="?",
        help="Job description text (or use -j/--job-file for file input)"
    )
    
    parser.add_argument(
        "-j", "--job-file",
        type=str,
        help="Path to file containing job description"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="updated_resume.tex",
        help="Output LaTeX file path (default: updated_resume.tex)"
    )
    
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "gemini"],
        default="openai",
        help="LLM provider to use (default: openai)"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for LLM provider (or set environment variable)"
    )
    
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF compilation (only generate LaTeX file)"
    )
    
    args = parser.parse_args()
    
    # Get job description
    if args.job_file:
        if not Path(args.job_file).exists():
            print(f"❌ Error: Job description file not found: {args.job_file}")
            sys.exit(1)
        with open(args.job_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
    elif args.job_description:
        job_description = args.job_description
    else:
        print("❌ Error: Job description required. Provide as argument or use -j/--job-file")
        sys.exit(1)
    
    # Check resume file exists
    if not Path(args.resume).exists():
        print(f"❌ Error: Resume file not found: {args.resume}")
        sys.exit(1)
    
    # Initialize and run
    try:
        updater = ResumeUpdater(llm_provider=args.provider, api_key=args.api_key)
        updater.process_resume(
            args.resume, 
            job_description, 
            args.output,
            compile_pdf=not args.no_pdf
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

