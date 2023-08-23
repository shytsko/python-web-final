from django.shortcuts import render


def home(request):
    context = {
        'title': 'Главная',
        'request': request,
    }
    return render(request, 'home/home.html', context)
