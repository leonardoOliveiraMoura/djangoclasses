from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    ...
    return render(request,'recipes/pages/home.html', context={
        'sendVariable':'informationVariable',
        })
    # http response

def func_sobre(request):
    return HttpResponse('Return of about route')
    # http response    
    
def func_contato(request):
    return HttpResponse('Return of contact route')
    # http response    