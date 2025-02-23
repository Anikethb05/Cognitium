import google.generativeai as genai
import os
import requests
import base64
from PIL import Image

# Load API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Generate text response
model = genai.GenerativeModel("gemini-1.5-flash") 
response = model.generate_content("Why is the sky blue?")
print(response.text)

# Download image from URL
image_url = "https://goo.gle/instrument-img"  # Ensure this is a direct image URL
response = requests.get(image_url, allow_redirects=True)

if response.status_code != 200:
    raise ValueError("Failed to fetch the image. Check the URL.")

# Convert image to base64
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

# Encode the image
encoded_image = encode_image(response.content)

# Correct request structure
contents = [
    {
        "role": "user",
        "parts": [
            {"text": "What is this image?"},
            {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
        ]
    }
]

# Generate response for the image
image_response = model.generate_content(contents)

# Print response
print(image_response.text)
