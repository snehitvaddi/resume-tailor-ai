"""
Build script to create executable from Streamlit app
Uses PyInstaller to package the application
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_executable():
    """Build executable using PyInstaller"""
    
    print("🔨 Building executable...")
    print("This may take a few minutes...")
    
    # PyInstaller options
    args = [
        'streamlit_app.py',
        '--name=ResumeUpdater',
        '--onefile',
        '--windowed',  # No console window (use --console if you want console)
        '--icon=NONE',  # Add icon path if you have one
        '--add-data=README.md;.',
        '--add-data=QUICK_START.md;.',
        '--hidden-import=streamlit',
        '--hidden-import=openai',
        '--hidden-import=google.generativeai',
        '--hidden-import=pdfplumber',
        '--hidden-import=subprocess',
        '--hidden-import=tempfile',
        '--collect-all=streamlit',
        '--collect-all=streamlit.web',
        '--collect-all=streamlit.runtime',
        '--noconfirm',
        '--clean'
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ Build complete!")
        print(f"📦 Executable location: dist/ResumeUpdater.exe")
        print("\n⚠️  Note: The executable will be large (~200-300MB) as it includes Python and all dependencies.")
    except Exception as e:
        print(f"\n❌ Build failed: {str(e)}")
        print("\nMake sure PyInstaller is installed: pip install pyinstaller")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()

