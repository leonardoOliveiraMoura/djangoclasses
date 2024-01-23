from django.http import HttpResponse
from django.shortcuts import render
from utils.recipes.factory import make_recipe

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
    
def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })  