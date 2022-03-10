from django.shortcuts import render
from django.http import HttpResponse
from .models import Friend

# Create your views here.

def index(request):
    num = Friend.objects.all().count()
    first = Friend.objects.all().first()
    last = Friend.objects.all().last()
    data = [num, first, last]
    params = {
        'title':'Hello',
        'data': data,
    }

    return render(request, 'hello/index.html', params)



