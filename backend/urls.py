from django.urls import path, include
from rest_framework.routers import DefaultRouter

#importando os serializadores
from .views import(
    ParagemViewSet,
    DisponibilidadeViewSet,
    obter_paradas_proximas,
)

#declarando o router para gerenciar as rotas
router = DefaultRouter()

router.register(
    'paragens', #rota 
    ParagemViewSet #
)

router.register(
    'disponibilidades',
    DisponibilidadeViewSet
)

urlpatterns = [
    path('paradas-proximas/', obter_paradas_proximas, name='paradas-proximas'),
    path('', include(router.urls)),
]