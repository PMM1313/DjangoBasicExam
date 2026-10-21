from django.shortcuts import render




def home(request): # simple at start
    return render(request, "dashboard/home.html")
