# Resume Updater - AI-Powered Resume Transformation

Transform your resume to perfectly match any job description using AI-powered storytelling and LaTeX formatting.

## 🎯 Features

- **🌐 Web Interface**: Beautiful Streamlit web app with file upload, copy-paste, and real-time progress tracking
- **📄 PDF Resume Extraction**: Automatically extracts text from PDF resumes
- **🤖 AI-Powered Transformation**: Uses OpenAI, Google Gemini, or Groq to rewrite your resume
- **🎯 Job Description Matching**: Analyzes job requirements and aligns your experience accordingly
- **📝 LaTeX Output**: Generates professional LaTeX-formatted resumes ready for manual PDF compilation
- **⚙️ Flexible API Options**: Choose between OpenAI, Gemini, or Groq (auto-detects from API key)
- **📊 Progress Tracking**: Real-time progress bars showing transformation stages
- **🔁 Iterative Refinement**: Offer up to 5 follow-up feedback turns to fine-tune the resume

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run streamlit_app.py
```

The app opens in your browser automatically at http://localhost:8501

### API Keys

Enter your API key in the sidebar. The app auto-detects the provider:
- **OpenAI**: Keys start with `sk-`
- **Google Gemini**: Keys start with `AIza`
- **Groq**: Keys start with `gsk_`

Get API keys from:
- OpenAI: https://platform.openai.com/account/api-keys
- Gemini: https://makersuite.google.com/app/apikey
- Groq: https://console.groq.com/keys

## 📦 Building Executable (.exe)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build Executable

```bash
python build_exe.py
```

### Step 3: Find Your Executable

- **Location:** `dist/ResumeUpdater.exe`
- **Size:** ~200-300MB (includes Python and all dependencies)
- **Ready to distribute!**

### Running the Executable

1. Navigate to `dist/` folder
2. Double-click `ResumeUpdater.exe`
3. App opens in browser automatically

**Note:** First run may trigger Windows Defender warning (normal for unsigned executables).

## 📋 How to Use

1. **Upload/Paste Resume**: Left side - PDF or text file
2. **Upload/Paste Job Description**: Right side - text or PDF file
3. **Enter API Key**: Sidebar - auto-detects provider
4. **Click "Transform Resume"**: Wait 1-2 minutes
5. **Download**: Get LaTeX (`updated_resume.tex`) and compile to PDF manually if needed
6. **Refine (Optional)**: Provide follow-up feedback up to 5 times for additional tweaks

## 🛠️ Project Structure

```
Resume-Updater/
├── streamlit_app.py     # Main web application
├── llm_service.py       # LLM API integration
├── pdf_extractor.py     # PDF text extraction
├── latex_generator.py   # LaTeX template & PDF compilation
├── main.py              # CLI version (optional)
├── build_exe.py         # Executable build script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## ⚙️ Requirements

- Python 3.8+
- API key from OpenAI, Gemini, or Groq
- MiKTeX (optional, for PDF compilation): https://miktex.org/

## 🐛 Troubleshooting

**"pdflatex not found"**
- Install MiKTeX: https://miktex.org/
- Or skip PDF compilation (LaTeX file will still be generated)

**"API key error"**
- Verify your API key is correct
- Check if the key has credits/access

**Executable won't run**
- Windows Defender may block it - click "More info" → "Run anyway"
- Ensure you have admin rights if needed

## 📚 License

Open source - feel free to use and modify!
