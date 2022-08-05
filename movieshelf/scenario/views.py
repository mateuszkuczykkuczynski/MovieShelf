from django.shortcuts import render


def startpage(request):
    return render(request, 'startpage.html')


def homepage(request):
    return render(request, 'homepage.html')