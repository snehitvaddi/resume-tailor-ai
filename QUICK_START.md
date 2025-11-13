# 🚀 Quick Start Guide

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Run the App
```bash
streamlit run streamlit_app.py
```

That's it! The app opens in your browser automatically.

---

## 📝 Where to Update What

### API Keys (Choose ONE method):

**Option A: In the Web App (Easiest)**
- Open the app → Sidebar → Enter API key in the text box

**Option B: Environment Variables (Recommended)**
- Windows PowerShell:
  ```powershell
  $env:OPENAI_API_KEY="your-key-here"
  ```
- Windows CMD:
  ```cmd
  set OPENAI_API_KEY=your-key-here
  ```
- Linux/Mac:
  ```bash
  export OPENAI_API_KEY="your-key-here"
  ```

**Option C: Create `.env` file** (in project root)
```
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
```

---

## 🔄 Simple Flow

```
1. START APP
   ↓
   streamlit run streamlit_app.py
   
2. UPLOAD/Paste RESUME
   ↓
   Left side: Upload PDF or paste text
   
3. UPLOAD/Paste JOB DESCRIPTION
   ↓
   Right side: Upload file or paste text
   
4. SELECT API & ENTER KEY
   ↓
   Sidebar: Choose OpenAI or Gemini
   Enter your API key
   
5. CLICK "Transform Resume"
   ↓
   Watch progress bar (1-2 minutes)
   
6. DOWNLOAD RESULT
   ↓
   Get LaTeX (.tex) and PDF files
```

---

## 📋 Complete Example

```bash
# Terminal 1: Install (one time only)
pip install -r requirements.txt

# Terminal 2: Run app
streamlit run streamlit_app.py

# Browser opens automatically → Use the web interface!
```

---

## 🎯 What Happens Behind the Scenes

1. **Extract Text** → Gets text from your resume PDF/file
2. **Transform Content** → AI rewrites resume to match job description
3. **Format to LaTeX** → Converts to professional LaTeX format
4. **Compile to PDF** → Creates final PDF file

**Total Time: 1-2 minutes**

---

## ⚠️ Troubleshooting

**"pdflatex not found"**
- Install MiKTeX (Windows): https://miktex.org/
- Or use `--no-pdf` flag in CLI version

**"API key error"**
- Make sure you entered the key correctly
- Check if it's valid and has credits

**App won't start**
- Make sure Streamlit is installed: `pip install streamlit`
- Check if port 8501 is available

---

## 📁 File Locations

- **Main App**: `streamlit_app.py` (web interface)
- **CLI Version**: `main.py` (command line)
- **Config**: API keys in sidebar or `.env` file
- **Output**: Downloads to your Downloads folder

---

**That's it! Just run `streamlit run streamlit_app.py` and you're good to go! 🎉**

