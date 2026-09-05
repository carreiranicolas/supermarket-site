from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_contas(request):
    return HttpResponse('Home Contas')
