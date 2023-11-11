# from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

# Create your views here.
def index(request) :
    todos = TODO.objects.all()
    content = {"todos" : todos }
    # return HttpResponse('My First Page')
    return render(request, 'master_todo_app/index.html', content)

def createtodo(request) :
    inputs = request.POST['todoContent']
    new_todo = TODO(content = inputs)
    new_todo.save()
    # return HttpResponse("create todo => " + inputs)
    return HttpResponseRedirect(reverse('index'))