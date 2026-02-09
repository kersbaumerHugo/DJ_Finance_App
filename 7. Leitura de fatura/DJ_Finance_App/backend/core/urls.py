from django.urls import path
from .views import resumo
from .views import lancamentos
from .views import lancamento_detail
from .views import meses


urlpatterns = [
   path('resumo/', resumo),
   #path('lancamentos', criar_lancamento),
   path("lancamentos/", lancamentos),
   path("lancamentos/<int:pk>/", lancamento_detail),
   path("lancamentos/meses/", meses)
   ]
