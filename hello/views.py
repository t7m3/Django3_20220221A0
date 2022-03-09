from django.shortcuts import render
from django.http import HttpResponse
from .models import Friend
from .forms import HelloForm


# Create your views here.

def index(request):
    data = Friend.objects.all()
    params = {
        'title':'Hello',
        'message':'all friends.',
        'form':HelloForm(),
        'data': data,
    }

    if (request.method == 'POST'):
        num=request.POST['id']
        item = Friend.objects.get(id=num)
        params['data'] = [item]
        params['form'] = HelloForm(request.POST)
    else:
        params['data'] = Friend.objects.all()

    return render(request, 'hello/index.html', params)



