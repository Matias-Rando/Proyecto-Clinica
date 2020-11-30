from django.conf import settings
from django.db import models

# Create your models here.

class Paciente(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    dni = models.IntegerField()
    telefono = models.CharField(max_length=64)
    direccion = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    # Método para mostrar el atributo nombre en la lista desplegable
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Asistencia(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Turno(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()


class Categoria(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64)
    precio = models.IntegerField()
    detalle = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Estado(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Tipopago(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Pedido(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipopago = models.ForeignKey(Tipopago, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    total = models.IntegerField()
    fechaentrega = models.DateField()

class Distancia(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Lado(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Armazon(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Subpedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    distancia = models.ForeignKey(Distancia, on_delete=models.CASCADE)
    lado = models.ForeignKey(Lado, on_delete=models.CASCADE)
    armazon = models.ForeignKey(Armazon, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Historial(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    titulo = models.CharField(max_length=64)
    detalle = models.TextField()
