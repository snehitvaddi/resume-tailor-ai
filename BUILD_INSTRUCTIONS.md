# Building Executable (.exe) for Resume Updater

## Prerequisites

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Build Steps

### Option 1: Using the Build Script (Recommended)

```bash
python build_exe.py
```

### Option 2: Manual PyInstaller Command

```bash
pyinstaller --name=ResumeUpdater --onefile --windowed --add-data="README.md;." --add-data="QUICK_START.md;." --collect-all=streamlit streamlit_app.py
```

## Output

- The executable will be created in the `dist/` folder
- File name: `ResumeUpdater.exe`
- Size: ~200-300MB (includes Python and all dependencies)

## Important Notes

1. **First Run**: The first time users run the .exe, Windows Defender may show a warning. This is normal for unsigned executables.

2. **Antivirus**: Some antivirus software may flag PyInstaller executables. You may need to:
   - Sign the executable with a code signing certificate
   - Submit to antivirus vendors for whitelisting

3. **Dependencies**: The executable is self-contained and doesn't require Python installation on the target machine.

4. **LaTeX**: Users still need to install MiKTeX separately for PDF compilation feature.

## Distribution

1. Create a zip file with:
   - `ResumeUpdater.exe`
   - `README.md`
   - `QUICK_START.md`

2. Optionally include:
   - Screenshots
   - Installation instructions for MiKTeX

## Alternative: Portable Version

For a smaller size, you can create a directory-based distribution:

```bash
pyinstaller --name=ResumeUpdater --onedir --windowed --add-data="README.md;." streamlit_app.py
```

This creates a folder with the executable and dependencies (easier to update individual files).

