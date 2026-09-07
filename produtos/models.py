from django.db import models
from core.models import ModelBase

# Create your models here.

class Categoria(ModelBase):
    nome = models.CharField(max_length=120)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Produto(ModelBase):
    nome = models.CharField(max_length=250)
    categoria = models.ForeignKey(
        to=Categoria,
        on_delete=models.PROTECT,
        related_name='produtos'
    ) # PROTECT impede a exclusão se tiver produto associado a Categoria
    estoque = models.PositiveIntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    class Meta:
        ordering = ['-adicionado_em']

    def preco_com_desconto(self):
        return self.preco * (1 - self.desconto/100)


    def __str__(self):
        return self.nome


