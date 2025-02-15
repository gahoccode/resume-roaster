from dotenv import load_dotenv
import os
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import Tool
import yaml

# Load environment variables from .env in the root
load_dotenv()

# Retrieve the Hugging Face token from the environment
hf_token = os.getenv("HF_TOKEN")

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Use this tool to provide your final answer"
    inputs = {
        "answer": {
            "type": "string",
            "description": "The final answer to the problem"
        }
    }
    output_type = "string"

    def forward(self, answer: str) -> str:
        return answer

class LinkedInScraperTool(Tool):
    name = "linkedin_scraper"
    description = "Scrapes LinkedIn profiles to extract professional information"
    inputs = {
        "linkedin_url": {
            "type": "string",
            "description": "The URL of the LinkedIn profile"
        }
    }
    output_type = "object"

    def forward(self, linkedin_url: str):
        # Dummy implementation; replace with actual scraping logic
        return {
            "experience": "10 years in industry",
            "skills": "Python, AI",
            "description": "Experienced professional with a robust background in technology."
        }

def create_agent():
    final_answer = FinalAnswerTool()
    linkedin_scraper = LinkedInScraperTool()
    
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
        custom_role_conversions=None,
    )

    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        
    agent = CodeAgent(
        model=model,
        tools=[linkedin_scraper, final_answer],
        max_steps=6,
        verbosity_level=1,
        prompt_templates=prompt_templates
    )
    
    return agent
