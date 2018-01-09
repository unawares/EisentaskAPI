from django.shortcuts import render

# Create your views here.

def headpage(request):
    return render(request, 'headpage/index.html')
