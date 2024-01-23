from django.urls import path
from recipes.views import home 
from . import views
#from recipes.views import func_contato
#from recipes.views import func_sobre

# hhtp Request

urlpatterns = [
    path('', views.home),
    path('recipes/<int:id>/', views.recipe),
    #path('sobre/', func_sobre),
    #path('contato/', func_contato)
]