
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def chatbot(request):
    response_text = None

    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            response = model.generate_content(query)
            response_text = response.text

    return render(request, "chat.html", {"response": response_text})

