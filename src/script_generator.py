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
def call_llm(prompt: str, model: str = "gemini-2.5-pro", max_tokens: int = 600) -> str:
    """
    Call the Gemini model and return generated text.
    """
    try:
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        print("-----------Model responding for prompt ------------------")
        print(response.text)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini model: {e}")


# ----------------------------
# 3️⃣ SCRIPT GENERATION
# ----------------------------
def generate_script(title: str, description: str, model: str = "gemini-2.5-flash") -> dict:
    """
    Generate a smooth 2-minute explainer script from title + description.
    Returns a dict:
    {
        "title": str,
        "script": str
    }
    """
    prompt = f"""
You are a professional script writer.  

Write a **smooth, engaging, and continuous 2-minute video script** that explains the following topic naturally, as if a narrator is speaking.  
Do **not** divide into segments, bullet points, or slides. Make it flow like a real video narration.

Title: {title}  
Description: {description}

Output **strictly as JSON**, nothing else:
{{
  "title": "{title}",
  "script": "..."
}}
"""

    llm_output = call_llm(prompt, model=model, max_tokens=700)

    # Attempt to extract JSON from the model output
    try:
        start = llm_output.index("{")
        end = llm_output.rindex("}") + 1
        json_str = llm_output[start:end]
        script = json.loads(json_str)
    except Exception:
        # Fallback
        script = {
            "title": title,
            "script": f"{description}. This video explains the topic in a smooth, engaging narration."
        }

    return script

