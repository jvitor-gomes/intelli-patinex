from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
