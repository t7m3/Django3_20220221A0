from unittest import result
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
            'result':''  # None
        }

    def get(self, request):
        return render(request, 'hello/index.html', self.params)

    def post(self, request):
        ch = request.POST.getlist('choice')
        result = 'selected:\n'  # index.htmlを{{result | linebreaksbr}}と変更しないと、改行しない。
        for item in ch:
            result += '  ・'  + item + '\n'
        # result += '\n'
        self.params['result'] = result
        self.params['form'] = HelloForm(request.POST)
        return render(request, 'hello/index.html', self.params)


