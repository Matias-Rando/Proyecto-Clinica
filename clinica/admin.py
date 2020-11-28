from django.contrib import admin
from .models import Estado, Tipopago, Distancia, Lado, Armazon, Asistencia
# Register your models here.
admin.site.register(Estado)
admin.site.register(Tipopago)
admin.site.register(Distancia)
admin.site.register(Lado)
admin.site.register(Armazon)
admin.site.register(Asistencia)