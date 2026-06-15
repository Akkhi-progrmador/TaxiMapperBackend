from django.contrib import admin

from .models import  Disponibilidade, Paragem

admin.site.register(Disponibilidade)
admin.site.register(Paragem)