"""
LLM Service Module
Handles API calls to OpenAI, Google Gemini, or Groq for resume transformation
"""

import os
from typing import Optional, List, Dict
from openai import OpenAI
import google.generativeai as genai


class LLMService:
    """Service for interacting with LLM APIs (OpenAI, Google Gemini, or Groq)"""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize LLM service
        
        Args:
            provider: "openai", "gemini", or "groq"
            api_key: API key for the provider (if None, reads from environment)
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4.1-2025-04-14"  # Using GPT-4.1 for best quality
        
        elif self.provider == "gemini":
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("Google API key not provided. Set GOOGLE_API_KEY environment variable.")
            genai.configure(api_key=self.api_key)
            # Use gemini-2.5-pro for best quality
            self.model = genai.GenerativeModel("gemini-2.5-pro")
        
        elif self.provider == "groq":
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("Groq API key not provided. Set GROQ_API_KEY environment variable.")
            # Groq uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            # Using meta-llama/llama-guard-4-12b as requested
            # Note: This is a guard model optimized for safety/content moderation
            # For general text generation, consider: llama-3.1-8b-instant or llama-3.3-70b-versatile
            self.model = "llama-3.1-8b-instant"
        
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai', 'gemini', or 'groq'")
    
    def transform_resume_content(self, resume_text: str, job_description: str) -> str:
        """Backward-compatible method that returns only the transformed resume."""
        response, _ = self.transform_resume_with_history(resume_text, job_description)
        return response

    def transform_resume_with_history(self, resume_text: str, job_description: str):
        """
        Transform resume and return conversation history for iterative refinement.

        Returns:
            Tuple[str, List[Dict[str, str]]]: (transformed resume, conversation history)
        """
        messages = self._build_initial_conversation(resume_text, job_description)
        response = self._chat(messages, temperature=0.6, max_tokens=8000)
        messages.append({"role": "assistant", "content": response})
        return response, messages

    def refine_with_feedback(self, conversation: List[Dict[str, str]], feedback: str):
        """
        Apply follow-up feedback to the existing conversation.

        Args:
            conversation: Chat message history returned by transform_resume_with_history/refine_with_feedback
            feedback: User feedback text

        Returns:
            Tuple[str, List[Dict[str, str]]]: (updated resume, updated conversation history)
        """
        follow_up_prompt = (
            "Follow-up feedback from the user:\n"
            f"{feedback.strip()}\n\n"
            "Please revise the ENTIRE resume accordingly. Keep all sections complete, maintain professional tone, "
            "ensure every previous company/role/project remains represented with 4-6 bullet points per role, and "
            "return the full updated resume text."
        )
        messages = [dict(m) for m in conversation]
        messages.append({"role": "user", "content": follow_up_prompt})
        response = self._chat(messages, temperature=0.6, max_tokens=8000)
        messages.append({"role": "assistant", "content": response})
        return response, messages

    def _build_initial_conversation(self, resume_text: str, job_description: str) -> List[Dict[str, str]]:
        base_prompt = f"""You are an expert resume writer with deep analytical skills. Your task is to completely transform the resume to perfectly match the job description while maintaining authenticity and professionalism.

JOB DESCRIPTION:
{job_description}

ORIGINAL RESUME:
{resume_text}

CRITICAL REQUIREMENTS - READ CAREFULLY:

STEP 1: COMPREHENSIVE ANALYSIS
- Extract ALL companies, roles, and positions from the original resume
- Identify the unique storyline and achievements for EACH company/role
- Map each experience to relevant job description requirements
- Note all technical skills, projects, and accomplishments mentioned

STEP 2: COMPLETE TRANSFORMATION (NOT SAMPLES)
- Transform EVERY single company/role experience - do not skip any
- For EACH position, create 4-6 detailed bullet points (not just 2-3)
- Ensure ALL sections are complete: Experience, Projects, Skills, Education
- Include ALL original companies and roles - nothing should be omitted

STEP 3: CONTENT QUALITY GUIDELINES
- Tone: Professional but friendly, confident but not arrogant
- Accuracy: Maintain all factual information (company names, dates, titles, locations)
- Quantification: Include specific numbers, metrics, percentages, and results where possible
- Relevance: Highlight experiences that directly align with job requirements
- Consistency: Use consistent formatting and verb tense (past tense for past roles)
- Authenticity: Do NOT over-exaggerate or fabricate achievements - stay truthful to the original

STEP 4: STRUCTURE REQUIREMENTS
- Professional Experience: List ALL roles with company, title, dates, and location
  * Each role must have 4-6 bullet points describing achievements
  * Focus on impact, results, and skills relevant to the job description
  * Use action verbs (Led, Built, Implemented, Optimized, etc.)
  * Bullet formatting rules:
    - The first bullet must summarize the overall scope and impact (team size, domain, tools, outcomes)
    - Each bullet must be a single concise line that fits on an A4 sheet at 12pt font
    - Use simple bullet markers (e.g., "- ") with no bolding or additional headings
- Technical Projects: Include ALL projects with detailed descriptions (3-4 bullet points each)
- Technical Skills: Comprehensive list matching job requirements (grouped by category)
- Education: Complete education section with degrees, institutions, dates, GPA if mentioned

OUTPUT FORMAT:
- Header with name, contact info, location, email, LinkedIn, GitHub
- Use \"### PROFESSIONAL EXPERIENCE\" for experience
- Use \"### TECHNICAL PROJECTS\" for projects
- Use \"### TECHNICAL SKILLS\" for skills (format like):

### TECHNICAL SKILLS

**Category 1:** skill1, skill2, skill3  
**Category 2:** skill4, skill5, skill6  

- Use \"### EDUCATION\" for education

IMPORTANT: This must be a COMPLETE, PROFESSIONAL resume ready for job applications - not a sample or partial version.

REASONING PROCESS - FOLLOW THESE STEPS:
1. First, mentally extract ALL companies and roles from the resume - list them all
2. For each role, identify 4-6 key achievements that match the job description
3. Transform each bullet point to highlight relevant skills and results
4. Ensure consistent professional tone throughout - friendly but not over-exaggerated
5. Verify ALL sections are complete before finalizing - check that nothing is missing

CRITICAL REMINDER: This is a REAL resume for a REAL job application. It must be complete, professional, detailed, and authentic."""

        return [
            {
                "role": "system",
                "content": (
                    "You are an expert resume writer specializing in ATS-optimized, storytelling resumes. "
                    "You ALWAYS provide complete, professional resumes with ALL experiences included - never samples, "
                    "never partial content. Every resume you create is ready for real job applications."
                ),
            },
            {"role": "user", "content": base_prompt},
        ]
    
    def format_to_latex(self, transformed_content: str, latex_template: str) -> str:
        """
        Stage 2: Format transformed content into LaTeX template structure
        
        Args:
            transformed_content: Transformed resume content from Stage 1
            latex_template: LaTeX template structure
            
        Returns:
            Complete LaTeX document with formatted content
        """
        prompt = f"""You are a LaTeX expert. Format the following resume content into the provided LaTeX template structure.

TRANSFORMED RESUME CONTENT:
{transformed_content}

LATEX TEMPLATE STRUCTURE:
{latex_template}

INSTRUCTIONS:
1. Extract all information from the transformed resume content
2. Properly format it into the LaTeX template structure
3. Use appropriate LaTeX commands for sections, subsections, bold text, lists, etc.
4. Ensure proper escaping of special LaTeX characters (%, &, $, #, _, ^, {{, }})
5. Maintain professional formatting and readability
6. Keep the template structure intact, only filling in the content
7. Use proper LaTeX list environments (itemize, enumerate) for bullet points
8. Format dates, names, and contact information appropriately

Return the complete LaTeX document ready to compile."""

        latex_messages = [
            {
                "role": "system",
                "content": "You are a LaTeX formatting expert specializing in resume documents. Format the complete resume content into proper LaTeX structure.",
            },
            {"role": "user", "content": prompt},
        ]
        return self._chat(latex_messages, temperature=0.3, max_tokens=8000)

    def _chat(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        if self.provider in {"openai", "groq"}:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        elif self.provider == "gemini":
            prompt_text = self._messages_to_prompt(messages)
            response = self.model.generate_content(prompt_text)
            return response.text.strip()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        formatted = []
        for message in messages:
            role = message.get("role", "user").upper()
            content = message.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n\n".join(formatted)

