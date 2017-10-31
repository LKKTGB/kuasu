from django.shortcuts import render, redirect


def home(request):
    return render(request, 'thiamsu/home.html')


def search(request):
    query = request.GET.get('q', '')
    if query == '':
        return redirect('/')

    return render(request, 'thiamsu/search_result.html', {
        'query': query,
    })
