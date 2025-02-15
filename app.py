import gradio as gr
import io
from PyPDF2 import PdfReader
from app import create_agent

def extract_text_from_pdf(file_obj) -> str:
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def process_resume(input_method, resume_text, pdf_file):
    if input_method == "Text":
        text = resume_text
    else:
        if pdf_file is None:
            return "No PDF uploaded."
        # Check if pdf_file is a string (i.e. a file path) or a file-like object
        if isinstance(pdf_file, str):
            with open(pdf_file, "rb") as f:
                file_bytes = f.read()
        else:
            file_bytes = pdf_file.read()
        file_obj = io.BytesIO(file_bytes)
        text = extract_text_from_pdf(file_obj)
    
    if not text.strip():
        return "No resume text found."
    
    agent = create_agent()
    # Instruct the agent to roast the resume using the resume text.
    response = agent.run(f"Roast this resume: {text}")
    return response


def toggle_inputs(method):
    if method == "Text":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

with gr.Blocks() as demo:
    gr.Markdown("# Resume Roaster")
    gr.Markdown("Enter your resume as text or upload a PDF to receive a humorous, professional roast!")
    
    input_method = gr.Radio(choices=["Text", "PDF"], label="Input Method", value="Text")
    resume_text = gr.Textbox(label="Resume Text", lines=10, visible=True)
    pdf_file = gr.File(label="Upload Resume PDF", file_types=[".pdf"], visible=False)
    output = gr.Textbox(label="Roast Result", lines=10)
    submit_btn = gr.Button("Roast It!")
    
    input_method.change(fn=toggle_inputs, inputs=input_method, outputs=[resume_text, pdf_file])
    submit_btn.click(fn=process_resume, inputs=[input_method, resume_text, pdf_file], outputs=output)
    
demo.launch(share=True)