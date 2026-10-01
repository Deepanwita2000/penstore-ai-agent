from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def chatbot(request):
    return render(request, "chatbot.html")