import imp
from pyexpat import model
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Friend
from .forms import FriendForm
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import FindForm
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max

# Create your views here.

class FriendList(ListView):
    model = Friend

class FriendDetail(DetailView):
    model = Friend

def index(request):
    data = Friend.objects.all()

    re1 = Friend.objects.aggregate(Count('age'))
    re2 = Friend.objects.aggregate(Sum('age'))
    re3 = Friend.objects.aggregate(Avg('age'))
    re4 = Friend.objects.aggregate(Min('age'))
    re5 = Friend.objects.aggregate(Max('age'))

    msg = 'count:' + str(re1['age__count']) \
            + '<br>Sum:' + str(re2['age__sum']) \
            + '<br>Average:' + str(re3['age__avg']) \
            + '<br>Min:' + str(re4['age__min']) \
            + '<br>Max:' + str(re5['age__max'])

    params = {
        'title':'Hello',
        'message':msg,
        'data': data,
    }
    return render(request, 'hello/index.html', params)

def find(request):
    if(request.method == 'POST'):
        msg = 'search result'
        form = FindForm(request.POST)
        find = request.POST['find']
        list = find.split()
        data = Friend.objects.all()[int(list[0]):int(list[1])]
        msg = 'Result: ' + str(data.count())
    else:
        msg = 'search words...'
        form = FindForm()
        data = Friend.objects.all()
    
    params = {
        'title': 'Hello',
        'message': msg,
        'form':form,
        'data':data
    }
    return render(request, 'hello/find.html', params)

# create model
def create(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
        
    params = {
        'title': 'Hello',
        'form':FriendForm(),        
    }
    return render(request, 'hello/create.html', params)

def edit(request, num):
    obj = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
        
    params = {
        'title': 'Hello',
        'id':num,
        'form': FriendForm(instance=obj)
    }
    return render(request, 'hello/edit.html', params)

def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')

    params = {
        'title': 'Hello',
        'id':num,
        'obj': friend,
    }
    return render(request, 'hello/delete.html', params)