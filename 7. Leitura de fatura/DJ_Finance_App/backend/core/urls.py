from django.urls import path
from .views import resumo

urlpatterns = [
   path('resumo', resumo),
   path('lancamentos', criar_lancamento)
   ]
