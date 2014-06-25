# Create your views here.
from django.shortcuts import render


def about(request):

    page = request.GET.get('page', '1')
    return render(request, "about/about.html", {'page' : page})

