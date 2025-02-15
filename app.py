from smolagents import CodeAgent, HfApiModel, tool
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI
import re
import yaml

@tool
def select_longest_answer(question: str) -> str:
    """A tool that selects the longest answer from multiple choice questions.
    
    Args:
        question: The question text containing multiple choice options
    """
    def extract_options(question_text):
        # Common patterns for multiple choice options
        patterns = [
            r'[A-D]\)\s*(.*?)(?=[A-D]\)|$)',  # A) format
            r'[A-D]\.\s*(.*?)(?=[A-D]\.|$)',   # A. format
            r'\([A-D]\)\s*(.*?)(?=\([A-D]\)|$)' # (A) format
        ]
        
        for pattern in patterns:
            options = re.findall(pattern, question_text)
            if options:
                return [opt.strip() for opt in options]
        
        # If no pattern matches, split by newlines and try to find options
        lines = question_text.split('\n')
        options = []
        for line in lines:
            if re.match(r'^[A-D][\)\.]\s*\w+', line):
                option = re.sub(r'^[A-D][\)\.]\s*', '', line)
                options.append(option.strip())
        
        return options

    def count_words(text):
        """Count the number of words in a text string."""
        words = re.sub(r'[^\w\s]', '', text).split()
        return len(words)

    def find_longest_answer(options):
        """Find the option with the most words."""
        if not options:
            return None
            
        word_counts = [(opt, count_words(opt)) for opt in options]
        return max(word_counts, key=lambda x: x[1])[0]

    def get_answer_letter(question_text, longest_answer):
        """Get the letter (A, B, C, D) corresponding to the longest answer."""
        options = extract_options(question_text)
        if not options:
            return None
            
        for i, option in enumerate(options):
            if option == longest_answer:
                return chr(65 + i)  # Convert 0->A, 1->B, etc.
        
        return None

    # Extract and process the options
    options = extract_options(question)
    if not options:
        return "Could not extract answer options from the question."

    # Find the longest answer and its letter
    longest_answer = find_longest_answer(options)
    answer_letter = get_answer_letter(question, longest_answer)
    
    # Calculate confidence based on word count difference
    word_counts = [count_words(opt) for opt in options]
    max_words = max(word_counts)
    
    return f"Selected option {answer_letter} as it is the longest answer with {max_words} words.\nFull answer: {longest_answer}"

def initialize_agent():
    final_answer = FinalAnswerTool()

    # Initialize the model
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
        custom_role_conversions=None,
    )

    # Load prompt templates
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)

    # Initialize the agent
    agent = CodeAgent(
        model=model,
        tools=[select_longest_answer, final_answer],
        max_steps=6,
        verbosity_level=1,
        grammar=None,
        planning_interval=None,
        name="LongestAnswerSelector",
        description="An agent that selects the longest answer in multiple choice questions",
        prompt_templates=prompt_templates
    )
    
    return agent

if __name__ == "__main__":
    agent = initialize_agent()
    GradioUI(agent).launch()