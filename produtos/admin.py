from django.contrib import admin
from .models import Categoria, Produto

# Register your models here.

#TODO

# Adicionar a linkagem de clicar em uma categoria e ser direcionado para o admin
# de produtos com os produtos daquela categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'adicionado_em']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'preco',
        'desconto',
        'estoque',
        'adicionado_em'
    ]

    search_fields = [
        'nome'
    ]
