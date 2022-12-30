from django.shortcuts import render

# Create your views here.


def crawl(request):

    return render(request, 'scraper/index.html')
