"""
PDF Text Extraction Module
Extracts text from PDF resume files
"""

import pdfplumber
from pathlib import Path
from typing import Optional


class PDFExtractor:
    """Extract text content from PDF resume files"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {pdf_path.suffix}")
        
        text_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            
            return "\n\n".join(text_content)
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_from_text_file(self, text_path: str) -> str:
        """
        Read text from a text file (for cases where resume is already in text format)
        
        Args:
            text_path: Path to the text file
            
        Returns:
            Text content as a string
        """
        text_path = Path(text_path)
        
        if not text_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_path}")
        
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")

