import yaml
import os
from smolagents import CodeAgent, HfApiModel, OpenAIServerModel
from smolagents.tools import Tool
from tools.resumescraper import ResumeScraperTool
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


# Load environment variables from .env file if it exists
load_dotenv()

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Use this tool to provide your final roast"
    inputs = {
        "answer": {
            "type": "string",
            "description": "The final roast for the resume"
        }
    }
    output_type = "string"

    def forward(self, answer: str) -> str:
        return answer

def create_agent():
    final_answer = FinalAnswerTool()
    resume_scraper = ResumeScraperTool()
    
    # Get model type from environment variable (default to "openai")
    model_type = os.getenv("MODEL_TYPE", "openai").lower()
    
    if model_type == "ollama":
        # Use OpenAIServerModel for Ollama (compatible with OpenAI API format)
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        # Create a model that uses Ollama's API (which is OpenAI-compatible)
        model = OpenAIServerModel(
            model_id=ollama_model,
            api_base=f"{ollama_url}/v1",
            max_tokens=2000,
            temperature=0.7
        )
    elif model_type == "openai":
        # Use OpenAI API
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Get OpenAI model name from environment variable or use a default
        openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        model = OpenAIServerModel(
            model_id=openai_model,
            api_key=openai_api_key,
            max_tokens=2000,
            temperature=0.7
        )
    else:
        # Use the original Hugging Face model as fallback
        model = HfApiModel(
            max_tokens=2096,
            temperature=0.7,
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
            custom_role_conversions=None,
        )
        
        # If HF_API_KEY is provided, use it
        hf_api_key = os.getenv("HF_API_KEY")
        if hf_api_key:
            client = InferenceClient(token=hf_api_key)
            model.client = client
        else:
            # Otherwise use the original endpoint
            client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")
            model.client = client

    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        
    agent = CodeAgent(
        model=model,
        tools=[resume_scraper, final_answer],
        max_steps=1,
        verbosity_level=1,
        prompt_templates=prompt_templates
    )
    
    return agent