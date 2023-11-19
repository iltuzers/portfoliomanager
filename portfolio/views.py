from django.shortcuts import render
from .models import Stock, Option, Portfolio


def index(request):
    return render(request, 'portfolio/index.html', {})
