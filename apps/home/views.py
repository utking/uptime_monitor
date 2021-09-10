from django.shortcuts import render, redirect


def index(request):
    return redirect('/monitor')


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})

