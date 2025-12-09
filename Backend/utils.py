import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY is missing in environment variables.")

genai.configure(api_key=api_key)


def detect_language(code_snippet):
    """Detects the programming language of the given code."""
    try:
        # Use the correct model ID (usually "models/gemini-1.5-pro" or "models/text-bison-001")
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = model.generate_content(
            f"Detect the programming language of this code:\n{code_snippet}"
        )
        return response.text.strip()
    except Exception as e:
        return f"Error in language detection: {str(e)}"


def generate_documentation(code_snippet):
    """Generates detailed documentation using Gemini."""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = model.generate_content(
            f"Generate detailed documentation for the following code:\n{code_snippet}"
        )

        print("Raw Gemini Response:", response.text)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Error in generating documentation: {str(e)}"