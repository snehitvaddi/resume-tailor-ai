"""
Streamlit Web Application for Resume Updater
Provides a user-friendly web interface for resume transformation
"""

import streamlit as st
import os
from pathlib import Path
import tempfile
from typing import Tuple, Optional
from pdf_extractor import PDFExtractor
from llm_service import LLMService
from latex_generator import LaTeXGenerator


# Page configuration
st.set_page_config(
    page_title="Resume Updater - AI-Powered Resume Transformation",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def detect_api_provider(api_key: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Automatically detect API provider based on key format
    
    Returns:
        Tuple of (provider_name, provider_code)
    """
    if not api_key:
        return None, None
    
    api_key = api_key.strip()
    
    # OpenAI keys start with "sk-"
    if api_key.startswith("sk-"):
        return "OpenAI (GPT-4.1)", "openai"
    
    # Google API keys start with "AIza"
    elif api_key.startswith("AIza"):
        return "Google Gemini (2.5 Pro)", "gemini"
    
    # Groq API keys start with "gsk_" (common pattern)
    elif api_key.startswith("gsk_"):
        return "Groq (Llama Guard 4)", "groq"
    
    # Unknown format
    return None, None


def initialize_session_state():
    """Initialize session state variables"""
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'latex_output' not in st.session_state:
        st.session_state.latex_output = None
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'followups_used' not in st.session_state:
        st.session_state.followups_used = 0
    if 'max_followups' not in st.session_state:
        st.session_state.max_followups = 5
    if 'processing_followup' not in st.session_state:
        st.session_state.processing_followup = False
    if 'transformed_content' not in st.session_state:
        st.session_state.transformed_content = None


def extract_text_from_uploaded_file(uploaded_file):
    """Extract text from uploaded file (PDF or text)"""
    extractor = PDFExtractor()
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            text = extractor.extract_text(tmp_path)
        else:
            text = extractor.extract_from_text_file(tmp_path)
        return text
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def main():
    """Main Streamlit application"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">📄 Resume Updater</p>', unsafe_allow_html=True)
    st.markdown("### Transform your resume to match any job description using AI")
    st.markdown("---")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Single API Key Input (auto-detects provider)
        api_key = st.text_input(
            "🔑 API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GROQ_API_KEY") or "",
            help="Enter your API key (OpenAI, Google Gemini, or Groq). The app will auto-detect the provider."
        )
        
        # Auto-detect provider from API key
        detected_provider, detected_provider_code = detect_api_provider(api_key)
        
        # Show detected provider or let user select
        if detected_provider:
            st.info(f"✅ Detected: **{detected_provider}**")
            provider = detected_provider_code
            api_provider_display = detected_provider
        else:
            if api_key:
                st.warning("⚠️ Could not detect API key type. Please ensure your key is correct.")
            # Manual selection if no key or detection failed
            api_provider_display = st.radio(
                "Choose LLM Provider:",
                ["OpenAI (GPT-4.1)", "Google Gemini (2.5 Pro)", "Groq (Llama Guard 4)"],
                help="Select manually if auto-detection failed"
            )
            if api_provider_display == "OpenAI (GPT-4.1)":
                provider = "openai"
            elif api_provider_display == "Google Gemini (2.5 Pro)":
                provider = "gemini"
            else:
                provider = "groq"
            
            # Warn if manual selection doesn't match key format
            if api_key:
                if provider == "openai" and not api_key.startswith("sk-"):
                    st.error("⚠️ Warning: Selected OpenAI but API key doesn't start with 'sk-'.")
                elif provider == "gemini" and not api_key.startswith("AIza"):
                    st.error("⚠️ Warning: Selected Gemini but API key doesn't start with 'AIza'.")
                elif provider == "groq" and not api_key.startswith("gsk_"):
                    st.warning("ℹ️ Groq keys typically start with 'gsk_'. Please verify your key is correct.")
        
        # Show key format hints
        with st.expander("💡 API Key Format"):
            st.markdown("""
            **OpenAI Keys:**
            - Start with `sk-`
            - Example: `sk-...`
            - Get from: https://platform.openai.com/account/api-keys
            
            **Google Gemini Keys:**
            - Start with `AIza`
            - Example: `AIza...`
            - Get from: https://makersuite.google.com/app/apikey
            
            **Groq Keys:**
            - Start with `gsk_`
            - Example: `gsk_...`
            - Get from: https://console.groq.com/keys
            - Model: meta-llama/llama-guard-4-12b (ultra-fast!)
            """)
        
        st.markdown("---")
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. Upload or paste your resume
        2. Upload or paste the job description
        3. Configure your API key
        4. Click 'Transform Resume'
        5. Download your updated resume!
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - **File Upload**: Supports PDF and text files
        - **Copy-Paste**: Quick option for text content
        - **API Keys**: Keep them secure, never share
        - **Processing**: Takes 1-2 minutes per resume
        """)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # Left column - Resume Input
    with col1:
        st.subheader("📄 Your Resume")
        
        resume_input_method = st.radio(
            "Input Method:",
            ["File Upload", "Copy-Paste"],
            key="resume_method",
            horizontal=True
        )
        
        if resume_input_method == "File Upload":
            uploaded_resume = st.file_uploader(
                "Upload Resume",
                type=["pdf", "txt"],
                help="Upload your resume as PDF or text file",
                key="resume_upload"
            )
            
            if uploaded_resume is not None:
                with st.spinner("Extracting text from resume..."):
                    try:
                        st.session_state.resume_text = extract_text_from_uploaded_file(uploaded_resume)
                        st.success(f"✅ Resume loaded! ({len(st.session_state.resume_text)} characters)")
                        with st.expander("Preview Resume Text"):
                            st.text(st.session_state.resume_text[:500] + "..." if len(st.session_state.resume_text) > 500 else st.session_state.resume_text)
                    except Exception as e:
                        st.error(f"Error extracting text: {str(e)}")
        else:
            resume_text_input = st.text_area(
                "Paste Resume Content",
                height=300,
                placeholder="Paste your resume content here...",
                key="resume_textarea"
            )
            if resume_text_input:
                st.session_state.resume_text = resume_text_input
                st.success(f"✅ Resume loaded! ({len(resume_text_input)} characters)")
    
    # Right column - Job Description Input
    with col2:
        st.subheader("💼 Job Description")
        
        jd_input_method = st.radio(
            "Input Method:",
            ["File Upload", "Copy-Paste"],
            key="jd_method",
            horizontal=True
        )
        
        if jd_input_method == "File Upload":
            uploaded_jd = st.file_uploader(
                "Upload Job Description",
                type=["txt", "pdf"],
                help="Upload job description as text or PDF file",
                key="jd_upload"
            )
            
            if uploaded_jd is not None:
                with st.spinner("Extracting text from job description..."):
                    try:
                        st.session_state.job_description = extract_text_from_uploaded_file(uploaded_jd)
                        st.success(f"✅ Job description loaded! ({len(st.session_state.job_description)} characters)")
                        with st.expander("Preview Job Description"):
                            st.text(st.session_state.job_description[:500] + "..." if len(st.session_state.job_description) > 500 else st.session_state.job_description)
                    except Exception as e:
                        st.error(f"Error extracting text: {str(e)}")
        else:
            jd_text_input = st.text_area(
                "Paste Job Description",
                height=300,
                placeholder="Paste the job description here...",
                key="jd_textarea"
            )
            if jd_text_input:
                st.session_state.job_description = jd_text_input
                st.success(f"✅ Job description loaded! ({len(jd_text_input)} characters)")
    
    st.markdown("---")
    
    # Process Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        process_button = st.button(
            "🚀 Transform Resume",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.processing
        )
    
    # Validation and Processing
    if process_button:
        # Validate inputs
        if not st.session_state.resume_text:
            st.error("❌ Please provide your resume first!")
            return
        
        if not st.session_state.job_description:
            st.error("❌ Please provide the job description!")
            return
        
        if not api_key:
            st.error("❌ Please enter your API key in the sidebar!")
            return
        
        # Start processing
        st.session_state.processing = True
        
        try:
            # Initialize services
            pdf_extractor = PDFExtractor()
            llm_service = LLMService(provider=provider, api_key=api_key)
            latex_generator = LaTeXGenerator()
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Extract text (already done, but show progress)
            status_text.text("Step 1/4: Resume text extracted ✅")
            progress_bar.progress(20)
            
            # Step 2: Transform resume content
            status_text.text("Step 2/4: Transforming resume content to match job description... (30-60 seconds)")
            progress_bar.progress(40)
            
            transformed_content, conversation_history = llm_service.transform_resume_with_history(
                st.session_state.resume_text,
                st.session_state.job_description
            )
            st.session_state.transformed_content = transformed_content
            st.session_state.conversation = conversation_history
            st.session_state.followups_used = 0
            st.session_state.max_followups = 5
            st.session_state.provider = provider
            st.session_state.api_key = api_key
            
            status_text.text("Step 2/4: Resume content transformed ✅")
            progress_bar.progress(60)
            
            # Step 3: Get LaTeX template
            status_text.text("Step 3/4: Loading LaTeX template...")
            progress_bar.progress(70)
            latex_template = latex_generator.get_default_template()
            status_text.text("Step 3/4: LaTeX template loaded ✅")
            progress_bar.progress(80)
            
            # Step 4: Format to LaTeX
            status_text.text("Step 4/4: Formatting content into LaTeX structure... (30-60 seconds)")
            progress_bar.progress(90)
            
            final_latex = llm_service.format_to_latex(transformed_content, latex_template)
            status_text.text("Step 4/4: Content formatted into LaTeX ✅")
            progress_bar.progress(95)
            
            # Save LaTeX to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tmp_tex:
                tmp_tex.write(final_latex)
                tmp_tex_path = tmp_tex.name
            
            st.session_state.latex_output = final_latex
            latex_file_path = Path(tmp_tex_path)
            
            progress_bar.progress(100)
            status_text.text("✨ Transformation Complete!")
            
            # Success message
            st.markdown("""
            <div class="success-box">
                <h3>✅ Resume Transformation Complete!</h3>
                <p>Your resume has been successfully transformed and is ready to download.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download buttons
            st.markdown("### 📥 Download Your Updated Resume")
            
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # LaTeX download
                st.download_button(
                    label="📝 Download LaTeX (.tex)",
                    data=final_latex,
                    file_name="updated_resume.tex",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_dl2:
                st.info("To convert to PDF, run `pdflatex updated_resume.tex` (requires a LaTeX distribution).")
            
            # Preview section
            with st.expander("📋 Preview Transformed Resume Content"):
                st.text(transformed_content)
            
            if st.session_state.latex_output:
                with st.expander("📐 Preview LaTeX Output"):
                    st.code(st.session_state.latex_output, language="latex")
            
            # Cleanup
            st.session_state.processing = False
            st.session_state.processing_followup = False
            
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.session_state.processing = False
            st.session_state.processing_followup = False
            progress_bar.empty()
            status_text.empty()

    # Follow-up refinement interface
    if st.session_state.transformed_content:
        st.markdown("---")
        st.subheader("🔁 Refine with Follow-Up Feedback")
        
        remaining = st.session_state.max_followups - st.session_state.followups_used
        st.caption(f"Follow-ups remaining: {remaining} / {st.session_state.max_followups}")
        
        feedback_disabled = remaining <= 0
        feedback = st.text_area(
            "Tell the assistant what to change (tone, emphasis, missing details, etc.)",
            height=160,
            disabled=feedback_disabled
        )
        
        apply_button = st.button(
            "✏️ Apply Feedback",
            key="apply_feedback_button",
            use_container_width=True,
            disabled=feedback_disabled or st.session_state.processing_followup
        )
        
        if feedback_disabled:
            st.info("You've reached the maximum number of follow-ups for this session (5).")
        
        if apply_button:
            if not feedback.strip():
                st.warning("Please enter specific feedback before applying.")
            else:
                st.session_state.processing_followup = True
                try:
                    with st.spinner("Applying feedback and updating resume..."):
                        llm_service = LLMService(provider=st.session_state.provider, api_key=st.session_state.api_key)
                        new_content, new_conversation = llm_service.refine_with_feedback(
                            st.session_state.conversation,
                            feedback
                        )
                        
                        latex_generator = LaTeXGenerator()
                        latex_template = latex_generator.get_default_template()
                        final_latex = llm_service.format_to_latex(new_content, latex_template)
                        
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tmp_tex:
                            tmp_tex.write(final_latex)
                        st.session_state.transformed_content = new_content
                        st.session_state.latex_output = final_latex
                        st.session_state.conversation = new_conversation
                        st.session_state.followups_used += 1
                        st.session_state.processing_followup = False
                        
                        st.success("✅ Follow-up applied! Updated resume is ready below.")
                except Exception as e:
                    st.session_state.processing_followup = False
                    st.error(f"❌ Follow-up failed: {str(e)}")
        
        # Show latest outputs
        with st.expander("📋 Latest Resume Content", expanded=False):
            st.text(st.session_state.transformed_content)
        
        if st.session_state.latex_output:
            with st.expander("📐 Latest LaTeX Output", expanded=False):
                st.code(st.session_state.latex_output, language="latex")
        
        download_col1, download_col2 = st.columns(2)
        with download_col1:
            if st.session_state.latex_output:
                st.download_button(
                    label="📝 Download Updated LaTeX",
                    data=st.session_state.latex_output,
                    file_name="updated_resume.tex",
                    mime="text/plain",
                    use_container_width=True
                )
        with download_col2:
            st.info("To convert to PDF, run `pdflatex updated_resume.tex` (requires LaTeX distribution).")


if __name__ == "__main__":
    main()

