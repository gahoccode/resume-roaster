import gradio as gr
from app import create_agent, extract_text_from_pdf

def create_ui():
    agent = create_agent()
    
    def process_inputs(text_input, pdf_file):
        # Prepare input
        if pdf_file:
            text_input = extract_text_from_pdf(pdf_file.name)
        
        if not text_input:
            return (
                "Please provide either text input or a PDF file.",
                "",
                ""
            )
        
        # Run the agent
        result = agent.run({
            "input": text_input,
            "chat_history": []
        })
        
        # Extract analysis from the result
        # Note: The actual structure might need adjustment based on how your agent returns results
        analysis = result.get("analysis", {})
        
        return (
            result.get("roast", "No roast generated"),
            f"Word Count: {analysis.get('length_analysis', {}).get('word_count', 0)}" if analysis else "",
            f"Buzzwords Detected: {', '.join(analysis.get('buzzwords', []))}" if analysis else ""
        )
    
    # Custom CSS for better styling
    custom_css = """
    .container {
        max-width: 1200px !important;
        margin: auto;
    }
    .main-header {
        color: #FF4B4B;
        text-align: center;
        padding: 20px;
        font-size: 2.5em !important;
        font-weight: bold;
    }
    .sub-header {
        color: #666;
        text-align: center;
        font-size: 1.2em !important;
        margin-bottom: 20px;
    }
    .output-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
    }
    .stats-box {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Resume Roaster Bot") as interface:
        gr.Markdown("# 🔥 Resume Roaster 3000 🔥", elem_classes=["main-header"])
        gr.Markdown(
            "Upload your resume and prepare to be professionally roasted! " +
            "We'll check for buzzwords, length, and other resume sins.",
            elem_classes=["sub-header"]
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="Paste your resume text here",
                    placeholder="Paste your resume content...",
                    lines=10
                )
                pdf_input = gr.File(
                    label="Or upload your resume PDF",
                    file_types=[".pdf"]
                )
                submit_btn = gr.Button(
                    "🔥 Roast My Resume!",
                    variant="primary"
                )
            
            with gr.Column(scale=1):
                output = gr.Textbox(
                    label="The Roast",
                    lines=10,
                    interactive=False,
                    elem_classes=["output-box"]
                )
                word_count = gr.Textbox(
                    label="Stats",
                    interactive=False,
                    elem_classes=["stats-box"]
                )
                buzzwords = gr.Textbox(
                    label="Buzzword Alert",
                    interactive=False,
                    elem_classes=["stats-box"]
                )
        
        submit_btn.click(
            fn=process_inputs,
            inputs=[text_input, pdf_input],
            outputs=[output, word_count, buzzwords]
        )
    
    return interface

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("HUGGINGFACE_API_KEY"):
        print("Error: HUGGINGFACE_API_KEY environment variable not set")
        print("Please set it with: export HUGGINGFACE_API_KEY='your-api-key'")
        exit(1)
    
    # Create and launch the interface
    interface = create_ui()
    interface.launch(share=True)