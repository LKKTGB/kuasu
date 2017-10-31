from django.shortcuts import render


def home(request):
    return render(request, 'thiamsu/home.html')


def search(request):
    return render(request, 'thiamsu/search_result.html')