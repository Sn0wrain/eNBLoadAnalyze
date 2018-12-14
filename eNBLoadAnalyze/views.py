from django.shortcuts import render

# Create your views here.
def index(request) :

    return render(request, 'index.html')

def uploadTDDLoadFile(request) :

    return render(request, 'dropzone_tdd.html')


def uploadFDDLoadFile(request):
    return render(request, 'dropzone_fdd.html')

def page_not_found(request):
    return render(request, '404.html')