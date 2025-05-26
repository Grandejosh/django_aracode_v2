from django.db import models

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