import google.generativeai as genai
import os

# Load API key from environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_KEY="AIzaSyAN5LQOqSimVBc2Jwq3FRUoLY_FUIn-tvE"

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash") 
response = model.generate_content("Why is the sky blue?")

print(response.text)
