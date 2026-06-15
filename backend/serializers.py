from rest_framework import serializers
from .models import Paragem, Disponibilidade


class ParagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragem
        fields = '__all__'
    
    '''{
            "id": 1,
            "nome": "São Paulo",
            "latitude": -8.83,
            "longitude": 13.23
        }'''
class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = '__all__'
        