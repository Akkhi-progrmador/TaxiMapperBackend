from django.db import models


class Paragem(models.Model):
    nome = models.CharField(max_length=25)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.nome

class Disponibilidade(models.Model):
    paragem = models.ForeignKey(
        Paragem,
        on_delete=models.CASCADE
    )

    quantidade_taxi= models.IntegerField(null=False, blank=False)
    tempo_min_espera = models.IntegerField(default= 5)
    disponivel = models.BooleanField(default=False)
    atualizado_em = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Disponivel: {self.disponivel}-{self.paragem}"
    