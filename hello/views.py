from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm

# Create your views here.

class HelloView(TemplateView):

    def __init__(self):
        self.params = {
            'title':'Hello',
            
            'form':HelloForm(),
            'result':''
        }

    def get(self, request):
        return render(request, 'hello/index.html', self.params)

    def post(self, request):
        if ('check' in request.POST):
            self.params['result'] = 'Checked!!'
        else:
            self.params['result'] = 'not checked...'
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)


