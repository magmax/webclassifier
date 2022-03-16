from django.shortcuts import render, redirect
from . import models

def index(request):
    context = {
        "websites": models.Website.objects.all()
    }
    return render(request, "index.html", context=context)

def spam(request, pk):
    website = models.Website.objects.get(pk=pk)
    website.spam()
    return redirect("index")

def jam(request, pk):
    website = models.Website.objects.get(pk=pk)
    website.jam()
    return redirect("index")

def process(request, pk):
    website = models.Website.objects.get(pk=pk)
    website.process()
    return redirect("index")

def processall(request):
    for website in models.Website.unprocessed():
        print(f"processing {website}")
        website.process()
    return redirect("index")
