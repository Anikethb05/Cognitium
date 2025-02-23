from django.contrib import admin
from django.urls import path
from .views import chatbot  # Import the chatbot view

urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),  # Define chatbot route

]
