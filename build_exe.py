"""
Build script to create executable from Streamlit app
Uses PyInstaller to package the application
"""

import subprocess
import sys
import os
from pathlib import Path

def build_executable():
    """Build executable using PyInstaller"""
    
    print("🔨 Building Resume Updater executable...")
    print("This may take 5-10 minutes...")
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")
    
    # Use spec file if it exists, otherwise use command line
    spec_file = Path("build_exe.spec")
    
    if spec_file.exists():
        print("📋 Using build_exe.spec configuration...")
        cmd = ["pyinstaller", "--clean", "--noconfirm", "build_exe.spec"]
    else:
        print("📋 Using default PyInstaller configuration...")
        cmd = [
            "pyinstaller",
            "--name=ResumeUpdater",
            "--onefile",
            "--console",  # Show console for Streamlit (helps with debugging)
            "--add-data=README.md;.",
            "--add-data=QUICK_START.md;.",
            "--hidden-import=streamlit",
            "--hidden-import=streamlit.web",
            "--hidden-import=streamlit.runtime",
            "--hidden-import=openai",
            "--hidden-import=google.generativeai",
            "--hidden-import=pdfplumber",
            "--collect-all=streamlit",
            "--noconfirm",
            "--clean",
            "streamlit_app.py"
        ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "="*60)
        print("✅ Build complete!")
        print("="*60)
        print(f"📦 Executable location: dist/ResumeUpdater.exe")
        print(f"📊 Size: ~200-300MB (includes Python + all dependencies)")
        print("\n💡 To run: Double-click ResumeUpdater.exe")
        print("\n⚠️  Note: First run may trigger Windows Defender warning.")
        print("   This is normal for unsigned executables.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code: {e.returncode}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Try running: pyinstaller --version")
        return False
    except Exception as e:
        print(f"\n❌ Build failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)

