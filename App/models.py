from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"
class Receta(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.URLField(blank=True, null=True)
    ingredientes = models.TextField()
    instrucciones = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Animal(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    especie = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre