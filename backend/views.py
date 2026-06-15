from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Paragem, Disponibilidade    
from .serializers import DisponibilidadeSerializer, ParagemSerializer
from math import radians, cos, sin, asin, sqrt


def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcular distância em km entre dois pontos usando Haversine."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


@api_view(['POST'])
@permission_classes([AllowAny])
def obter_paradas_proximas(request):
    try:
        user_latitude = float(request.data.get('latitude'))
        user_longitude = float(request.data.get('longitude'))
        distancia_max_km = float(request.data.get('distancia_max', 5))

        paradas = Paragem.objects.all()
        resultado = []

        for paragem in paradas:
            dist = calcular_distancia(
                user_latitude,
                user_longitude,
                paragem.latitude,
                paragem.longitude,
            )
            if dist <= distancia_max_km:
                disponibilidade = Disponibilidade.objects.filter(paragem=paragem).first()
                resultado.append({
                    'id': paragem.id,
                    'nome': paragem.nome,
                    'latitude': paragem.latitude,
                    'longitude': paragem.longitude,
                    'distancia_km': round(dist, 2),
                    'disponivel': disponibilidade.disponivel if disponibilidade else False,
                    'quantidade_taxi': disponibilidade.quantidade_taxi if disponibilidade else 0,
                    'tempo_espera': disponibilidade.tempo_min_espera if disponibilidade else 0,
                    'atualizado_em': disponibilidade.atualizado_em if disponibilidade else None,
                })

        resultado.sort(key=lambda item: item['distancia_km'])

        return Response(
            {
                'status': 'sucesso',
                'user_location': {
                    'latitude': user_latitude,
                    'longitude': user_longitude,
                },
                'paradas_proximas': resultado,
                'total': len(resultado),
            },
            status=status.HTTP_200_OK,
        )
    except (TypeError, ValueError):
        return Response(
            {'status': 'erro', 'mensagem': 'latitude e longitude inválidas.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exc:
        return Response(
            {'status': 'erro', 'mensagem': str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )



class ParagemViewSet(viewsets.ModelViewSet):
    queryset = Paragem.objects.all()
    serializer_class = ParagemSerializer


class DisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer