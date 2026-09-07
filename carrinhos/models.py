from django.db import models
from core.models import ModelBase
from produtos.models import Produto


# Create your models here.

class Carrinho(ModelBase):
    produtos = models.ManyToManyField(
        to=Produto,
        through="ItemCarrinho",
        related_name='carrinhos'
    )

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        to=Carrinho,
        related_name='itens_carrinho',
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        Produto,
        related_name='itens_carrinho',
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField(default=1)

    # Não adicionamos preço aqui por conta da lógica:
    # se mudar o preço do produto, deve mudar no carrinho,
    # então obteremos esse valor na tabela de produtos mesmo

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['carrinho', 'produto'],
                name='unico_produto_por_carrinho'
            )
        ]

    @property
    def subtotal(self):
        return self.produto.preco_com_desconto() * self.quantidade

        # Isso vai melhorar bastante, porque depois, lá na frente, será só fazer:
        # carrinho = Carrinho.objects.get(pk=1)
        # sum(item.subtotal for item in carrinho.itens_carrinho.all())