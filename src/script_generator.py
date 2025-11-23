import os
import json
import google.generativeai as genai

# ----------------------------
# 1️⃣ AUTHENTICATION
# ----------------------------
def setup_genai(api_key: str = None):
    """
    Configure the Google Generative AI (Gemini) client.
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No GEMINI_API_KEY or GOOGLE_API_KEY found in environment")

    genai.configure(api_key=api_key)
    return genai


# ----------------------------
# 2️⃣ LLM CALL
# ----------------------------
def call_llm(prompt: str, model: str = "gemini-2.5-flash", max_tokens: int = 600) -> str:
    """
    Call the Gemini model and return generated text.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini model: {e}")


# ----------------------------
# 3️⃣ SCRIPT GENERATION
# ----------------------------
def generate_script(title: str, description: str, model: str = "gemini-2.5-flash") -> dict:
    """
    Generate a structured explainer script from title + description.

    Returns a dict:
    {
        "title": str,
        "hook": str,
        "segments": [{"heading": str, "content": str, "diagram": str}],
        "cta": str
    }
    """
    prompt = f"""
    Generate a structured 3-minute explainer script for a video.

    Title: {title}
    Description: {description}

    Output format (JSON):
    {{
        "title": "...",
        "hook": "...",
        "segments": [
            {{"heading": "...", "content": "...", "diagram": "..."}}
        ],
        "cta": "..."
    }}

    Keep it concise and clear for slides + narration. Output valid JSON only.
    """

    llm_output = call_llm(prompt, model=model)

    # Try parsing JSON from LLM output
    try:
        script = json.loads(llm_output)
    except json.JSONDecodeError:
        # fallback dummy structure if LLM output is not valid JSON
        script = {
            "title": title,
            "hook": f"Hook for: {title}",
            "segments": [
                {"heading": "Segment 1", "content": description, "diagram": "chart1"},
                {"heading": "Segment 2", "content": "Explain details here", "diagram": "chart2"},
            ],
            "cta": "Subscribe for more!"
        }

    return script
