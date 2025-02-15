from smolagents.tools import Tool

class ResumeScraperTool(Tool):
    name = "resume_scraper"
    description = (
        "Parses a resume (in plain text) to extract key sections such as Summary, "
        "Experience, Education, and Skills. This tool expects the resume text to include "
        "section headers like 'Summary:', 'Experience:', 'Education:', and 'Skills:'."
    )
    inputs = {
        "resume_text": {
            "type": "string",
            "description": "The plain text of the resume"
        }
    }
    output_type = "object"

    def forward(self, resume_text: str) -> dict:
        # Basic extraction using simple markers; in a real-world case, you might want to use NLP.
        sections = {
            "summary": "Summary not found",
            "experience": "Experience not found",
            "education": "Education not found",
            "skills": "Skills not found"
        }
        lower_text = resume_text.lower()

        if "summary:" in lower_text:
            start = lower_text.index("summary:")
            # Assume the section ends at the next double newline or end of text
            end = lower_text.find("\n\n", start)
            sections["summary"] = resume_text[start + len("summary:"): end].strip() if end != -1 else resume_text[start + len("summary:"):].strip()

        if "experience:" in lower_text:
            start = lower_text.index("experience:")
            end = lower_text.find("\n\n", start)
            sections["experience"] = resume_text[start + len("experience:"): end].strip() if end != -1 else resume_text[start + len("experience:"):].strip()

        if "education:" in lower_text:
            start = lower_text.index("education:")
            end = lower_text.find("\n\n", start)
            sections["education"] = resume_text[start + len("education:"): end].strip() if end != -1 else resume_text[start + len("education:"):].strip()

        if "skills:" in lower_text:
            start = lower_text.index("skills:")
            end = lower_text.find("\n\n", start)
            sections["skills"] = resume_text[start + len("skills:"): end].strip() if end != -1 else resume_text[start + len("skills:"):].strip()

        return sections
