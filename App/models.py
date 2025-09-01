from django.db import models

# Create your models here.
class Receta(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.URLField(blank=True, null=True)
    ingredientes = models.TextField()
    instrucciones = models.TextField()

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Animal(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    especie = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre