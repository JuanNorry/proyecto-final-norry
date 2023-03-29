from django.db import models
from django.contrib.auth.models import User

class Componente(models.Model):
    tipo = models.CharField(max_length=100)
    modelo = models.TextField(max_length=200)
    descripcion = models.TextField(max_length=600)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to="componentes", null=True, blank=True)
    publisher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="publisher")

    @property
    def imagen_url(self):
        return self.imagen.url if self.imagen else ''
    
    def __str__(self):
        return f"{self.id} - {self.tipo} - {self.publisher.id}"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    mail = models.CharField(max_length=100, null=True)
    red_social = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(upload_to="avatares", null=True, blank=True)

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else ''

class Mensaje(models.Model):
    mensaje = models.TextField(max_length=1000, null=True)
    mail = models.EmailField(max_length=1000, null=True)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes", null=True)
