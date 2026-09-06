from django.db import models

class ModelBase(models.Model):
    adicionado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    excluido = models.BooleanField(default=False)
    excluido_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True