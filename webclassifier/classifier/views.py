from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def web(request):
    if request.method != "POST":
        raise Exception("not supported")
    models.Website.objects.create(
        external_id=request.POST['code'],
        url=request.POST['url'],
    )
    return redirect("index")
