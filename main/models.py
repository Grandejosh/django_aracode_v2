from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class CustomUser(AbstractUser):
    token = models.CharField(max_length=255, blank=True, null=True)
    used_token_count = models.IntegerField(default=0)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class EstadoContribuyente(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

class Contribuyente(models.Model):
    ruc = models.CharField(max_length=11)
    nombre_o_razon_social = models.CharField(max_length=255)
    estado_del_contribuyente = models.ForeignKey(EstadoContribuyente, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_o_razon_social

class TokenActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    used_token = models.IntegerField(default=0, verbose_name="Tokens usados")
    limit = models.IntegerField(default=10, verbose_name="Límite de tokens")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Actividad de Token"
        verbose_name_plural = "Actividades de Tokens"
        db_table = "token_activity"

    def __str__(self):
        return f"{self.user.username} - Usados: {self.used_token}/{self.limit}"
    

class ApiKey(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Identificador de la API Key
    key = models.CharField(max_length=255, unique=True)   # Token JWT generado
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # Opcional: Fecha de expiración

    def __str__(self):
        return f"{self.name} ({'active' if self.is_active else 'inactive'})"