import yaml
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import Tool
from tools.resumescraper import ResumeScraperTool
from huggingface_hub.inference_api import InferenceClient

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
    
    # Initialize a dedicated InferenceClient using the public endpoint.
    # This endpoint serves Llama3.2-3B-instruct and is less overloaded.
    client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")
    
    # Instantiate HfApiModel with our dedicated client.
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',  # Model ID remains, but the client is overridden
        custom_role_conversions=None,
        client=client
    )

    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        
    agent = CodeAgent(
        model=model,
        tools=[resume_scraper, final_answer],
        max_steps=6,
        verbosity_level=1,
        prompt_templates=prompt_templates
    )
    
    return agent
