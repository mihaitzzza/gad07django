from django.shortcuts import render


def homepage_view(request):
    return render(request, 'homepage.html', {
        "name": "Django"
    })
