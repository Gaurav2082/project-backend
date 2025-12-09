import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gemini_api(code_snippet):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Generate detailed documentation for the following code:\n{code_snippet}")

        print("Raw Gemini Response (Text):", response.text)  # Print raw text
        print("Full Gemini Response:", response)  # Print the full response object
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

# Example usage:
code = """
def my_function(x):
    return x * 2
"""

test_gemini_api(code)