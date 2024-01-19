from django.urls import path
from recipes.views import home 
#from recipes.views import func_contato
#from recipes.views import func_sobre

# hhtp Request

urlpatterns = [
    path('', home),
    #path('sobre/', func_sobre),
    #path('contato/', func_contato)
]