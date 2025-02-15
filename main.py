import gradio as gr
from app import create_agent

def roast_profile(linkedin_url):
    agent = create_agent()
    response = agent.run(
        f"Scrape this LinkedIn profile: {linkedin_url} and create a humorous but not mean-spirited roast based on their experience, skills, and description. Keep it professional and avoid personal attacks."
    )
    return response

demo = gr.Interface(
    fn=roast_profile,
    inputs=gr.Textbox(label="LinkedIn Profile URL"),
    outputs=gr.Textbox(label="Roast Result"),
    title="LinkedIn Profile Roaster",
    description="Enter a LinkedIn profile URL and get a humorous professional roast!",
    examples=[["https://www.linkedin.com/in/example-profile"]]
)

if __name__ == "__main__":
    demo.launch(share=True)
