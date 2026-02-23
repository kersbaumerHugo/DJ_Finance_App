from django.urls import path
from .views import analytics_financeiro
from .views import lancamentos
from .views import lancamento_detail
from .views import meses
from .views import upload_fatura
from .views import importar_fatura


urlpatterns = [
   path('analytics/', analytics_financeiro),
   #path('lancamentos', criar_lancamento),
   path("lancamentos/", lancamentos),
   path("lancamentos/<int:pk>/", lancamento_detail),
   path("lancamentos/meses/", meses),
   path('faturas/upload/', upload_fatura),
   path('faturas/importar/', importar_fatura)
   ]
