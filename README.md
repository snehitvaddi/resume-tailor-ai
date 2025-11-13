# Resume Updater - AI-Powered Resume Transformation

Transform your resume to perfectly match any job description using AI-powered storytelling and LaTeX formatting.

## 🎯 Features

- **🌐 Web Interface**: Beautiful Streamlit web app with file upload, copy-paste, and real-time progress tracking
- **📄 PDF Resume Extraction**: Automatically extracts text from PDF resumes
- **🤖 AI-Powered Transformation**: Uses GPT-4 or Gemini to rewrite your resume in a compelling storytelling format
- **🎯 Job Description Matching**: Analyzes job requirements and aligns your experience accordingly
- **📝 LaTeX Output**: Generates professional LaTeX-formatted resumes
- **📄 Automatic PDF Compilation**: Automatically compiles LaTeX to PDF using pdflatex (with cleanup of intermediate files)
- **⚙️ Flexible API Options**: Choose between OpenAI or Google Gemini
- **📊 Progress Tracking**: Real-time progress bars showing transformation stages
- **Two-Stage Processing**: 
  1. Content transformation (storytelling approach)
  2. LaTeX formatting and structure

## 🚀 Quick Start

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Choose your interface:**

   **Option A: Web Interface (Streamlit) - Recommended for beginners**
   ```bash
   streamlit run streamlit_app.py
   ```
   Then open your browser to the URL shown (usually http://localhost:8501)

   **Option B: Command Line Interface**
   ```bash
   python main.py resume.pdf "Job description"
   ```

4. **Set up API keys:**

   For OpenAI:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or for Google Gemini:
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```

   Alternatively, create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   GOOGLE_API_KEY=your-api-key-here
   ```

### Usage

**Basic usage:**
```bash
python main.py resume.pdf "Job description text here"
```

**With job description from file:**
```bash
python main.py resume.pdf -j job_description.txt
```

**Using Google Gemini instead of OpenAI:**
```bash
python main.py resume.pdf "Job description" --provider gemini
```

**Custom output path:**
```bash
python main.py resume.pdf "Job description" -o my_custom_resume.tex
```

**Skip PDF compilation (only generate LaTeX):**
```bash
python main.py resume.pdf "Job description" --no-pdf
```

## 📋 Command-Line Options

```
positional arguments:
  resume                Path to resume file (PDF or text file)
  job_description       Job description text (or use -j/--job-file)

optional arguments:
  -h, --help           Show help message
  -j, --job-file       Path to file containing job description
  -o, --output         Output LaTeX file path (default: updated_resume.tex)
  --provider           LLM provider: openai or gemini (default: openai)
  --api-key            API key for LLM provider
  --no-pdf             Skip PDF compilation (only generate LaTeX file)
```

## 🔄 How It Works

1. **Text Extraction**: Extracts text from your PDF or text resume
2. **Stage 1 - Content Transformation**: 
   - Analyzes job description requirements
   - Rewrites resume content using storytelling approach
   - Highlights relevant experiences and achievements
   - Maintains factual accuracy while enhancing descriptions
3. **Stage 2 - LaTeX Formatting**:
   - Formats transformed content into professional LaTeX structure
   - Handles special characters and formatting
   - Produces compile-ready LaTeX document
4. **Automatic PDF Compilation** (optional):
   - Automatically compiles LaTeX to PDF using `pdflatex`
   - Runs compilation twice for proper cross-references
   - Cleans up intermediate files (.log, .aux, etc.)

## 📝 PDF Compilation

The application **automatically compiles LaTeX to PDF** by default using `pdflatex`. 

### Prerequisites

You'll need a LaTeX distribution installed:

- **Windows**: Install [MiKTeX](https://miktex.org/) (recommended)
- **Linux**: `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-extra`
- **macOS**: Install MacTeX or use `brew install --cask mactex`

### Manual Compilation

If you want to skip automatic compilation (use `--no-pdf` flag), you can manually compile:

```bash
pdflatex updated_resume.tex
```

The application automatically cleans up intermediate files (.log, .aux, .out, etc.) after compilation.

## 🛠️ Project Structure

```
resume_updater/
├── main.py              # CLI application entry point
├── streamlit_app.py     # Web interface (Streamlit)
├── pdf_extractor.py     # PDF text extraction module
├── llm_service.py       # LLM API integration (OpenAI/Gemini)
├── latex_generator.py   # LaTeX template management
├── templates/           # LaTeX template directory
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ⚙️ Configuration

### LLM Providers

- **OpenAI (GPT-4o)**: Best quality, recommended for professional resumes
- **Google Gemini (Flash)**: Cost-effective, faster processing

### Custom Templates

You can create custom LaTeX templates in the `templates/` directory and load them using the `LaTeXGenerator` class.

## 🖥️ Web Interface (Streamlit)

The Streamlit app provides a user-friendly web interface with:

- **File Upload or Copy-Paste**: Upload PDF/text files or paste content directly
- **API Provider Selection**: Choose between OpenAI or Google Gemini
- **Real-time Progress**: See progress bars for each transformation stage
- **Preview & Download**: Preview transformed content and download LaTeX/PDF files

**To run the web interface:**
```bash
streamlit run streamlit_app.py
```

The app will open in your default browser automatically.

## 📄 Example

**Using Web Interface:**
1. Run `streamlit run streamlit_app.py`
2. Upload your resume and job description (or paste text)
3. Select API provider and enter API key
4. Click "Transform Resume"
5. Download your updated resume!

**Using Command Line:**
```bash
# Transform resume for a Data Engineer position (automatically generates PDF)
python main.py "Snehit Vaddi Data Resume.pdf" -j data_engineer_job.txt -o data_engineer_resume.tex

# Or skip PDF compilation if you prefer manual compilation
python main.py "Snehit Vaddi Data Resume.pdf" -j data_engineer_job.txt --no-pdf
```

## 🔒 Privacy & Security

- All API calls are made directly to OpenAI/Google servers
- No data is stored locally except your input files and output
- API keys should be kept secure (use environment variables)

## 🐛 Troubleshooting

**Error: API key not found**
- Make sure you've set the environment variable or passed `--api-key`
- Check that the API key is valid

**Error: PDF extraction failed**
- Ensure the PDF is not password-protected
- Try converting to text file first

**Error: pdflatex not found**
- Install a LaTeX distribution:
  - Windows: [MiKTeX](https://miktex.org/)
  - Linux: `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-extra`
  - macOS: Install MacTeX or `brew install --cask mactex`
- Ensure `pdflatex` is in your system PATH

**Error: PDF compilation failed**
- Check that the generated `.tex` file is valid
- Review LaTeX compilation errors in the output
- Try compiling manually: `pdflatex your_file.tex`

## 📚 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

