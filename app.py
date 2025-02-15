import os
from typing import List, Dict, Any, Optional
import gradio as gr
from smolagents import CodeAgent, FinalAnswerTool, HfApiModel
from tools.resume_tools import TextExtractionTool, ResumeCriticTool
import yaml
import fitz  # PyMuPDF
import json

def create_agent():
    # Initialize tools
    final_answer = FinalAnswerTool()
    text_extraction = TextExtractionTool()
    resume_critic = ResumeCriticTool()
    
    # Setup model
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
        custom_role_conversions=None,
    )
    
    # Load prompts
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
    
    # Create the agent
    agent = CodeAgent(
        model=model,
        tools=[final_answer, text_extraction, resume_critic],
        max_steps=6,
        verbosity_level=1,
        grammar=None,
        planning_interval=None,
        name="ResumeRoaster",
        description="An agent that analyzes and roasts resumes",
        prompt_templates=prompt_templates
    )
    
    return agent

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text