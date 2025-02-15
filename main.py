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
        # pdf_file may be a file path or a file-like object; handle accordingly
        if isinstance(pdf_file, str):
            with open(pdf_file, "rb") as f:
                file_bytes = f.read()
        else:
            # Ensure the file pointer is at the beginning
            pdf_file.seek(0)
            file_bytes = pdf_file.read()
        file_obj = io.BytesIO(file_bytes)
        text = extract_text_from_pdf(file_obj)
    
    if not text.strip():
        return "No resume text found."
    
    agent = create_agent()
    # Use the agent to roast the resume.
    response = agent.run(f"Roast this resume: {text}")
    return response

def toggle_inputs(method):
    # Updated order: pdf_file first, then resume_text.
    if method == "Text":
        return gr.update(visible=False), gr.update(visible=True)
    else:
        return gr.update(visible=True), gr.update(visible=False)

css_custom = """
footer {visibility: hidden;}
.center { 
  margin: 0 auto; 
  text-align: center; 
}
@keyframes beat {
  0%, 20%, 40%, 60%, 80%, 100% { transform: scale(1); }
  10%, 30%, 50%, 70%, 90% { transform: scale(1.2); }
}
.beating-heart {
  display: inline-block;
  animation: beat 2s infinite;
}
.fire-effect {
  font-size: 2.5em;
  font-weight: bold;
  background: linear-gradient(45deg, red, orange, yellow);
  background-size: 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: fireAnimation 3s linear infinite;
}
@keyframes fireAnimation {
  0% { background-position: 0%; }
  50% { background-position: 100%; }
  100% { background-position: 0%; }
}
/* Center the radio button options */
div[role="radiogroup"] {
  display: flex;
  justify-content: center;
}
"""

# Inject the CSS via the head parameter
head_injection = f"<style>{css_custom}</style>"

with gr.Blocks(head=head_injection) as demo:
    with gr.Column(elem_classes="center"):
        gr.Markdown('<div class="fire-effect">Resume Roaster</div>')
        gr.Markdown("Upload your resume as a PDF (default) or paste the text to receive a humorous, professional roast!")
    
        # Reordered radio choices so that PDF is first.
        input_method = gr.Radio(choices=["PDF", "Text"], label="Input Method", value="PDF")
        # PDF upload comes first
        pdf_file = gr.File(label="Upload Resume PDF", file_types=[".pdf"], visible=True)
        resume_text = gr.Textbox(label="Resume Text", lines=10, visible=False)
        output = gr.Textbox(label="Roast Result", lines=10)
        submit_btn = gr.Button("Roast It!")
    
    # Adjust toggle outputs to match new order.
    input_method.change(fn=toggle_inputs, inputs=input_method, outputs=[pdf_file, resume_text])
    submit_btn.click(fn=process_resume, inputs=[input_method, resume_text, pdf_file], outputs=output)
    
    gr.Markdown(
        """
        <div id="custom_footer" style="text-align: center; margin-top: 20px; font-size: 14px;">
          Made with <span class="beating-heart">💓</span> by Kuber Mehta<br>
          All jokes are crafted in good humor to provide professional levity.
        </div>
        """
    )

demo.launch(share=False)
