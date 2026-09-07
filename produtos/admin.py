from django.contrib import admin, messages
from django.utils.translation import ngettext # Usado para texto singular e plural
from .models import Categoria, Produto

admin.site.site_header = 'Supermarket Painel'
admin.site.index_title = 'Administração do Supermarket'

# Register your models here.


#FILTROS PERSONALIZADOS:

# https://docs.djangoproject.com/en/6.1/ref/contrib/admin/filters/

class EstoqueFiltro(admin.SimpleListFilter):
    title = "estoque"
    parameter_name = "estoque" 

    def lookups(self, request, model_admin):
        # O valor de lookup será selecionado pelo usuário e em
        # def queryset iremos definir o que vai retornar a partir do selecionado

        return [
            ("baixo", "Baixo (< 10)"), #Valor à esquerda é o código e à direita é o que
            # aparece no filtro
            ("medio", "Medio (<= 10 & < 15)"),
            ("alto", "Alto (<= 15)")
        ]

    def queryset(self, request, queryset):
        if self.value() == "baixo":
            return queryset.filter(
                estoque__lt=10
            )

        if self.value() == "medio":
            return queryset.filter(
                estoque__gte=10,
                estoque__lt=15
            )

        if self.value() == "alto":
            return queryset.filter(
                estoque__gte=15
            )

# DEFININDO INLINES

class ProdutoInline(admin.TabularInline):
    model = Produto
    extra = 0 # extra = 0 remove as linhas em branco extras que o Django mostra por padrão.
    fields = ['nome', 'preco', 'estoque', 'imagem']

# MODELSADMIN

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'adicionado_em']
    inlines = [ProdutoInline]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'categoria',
        'preco',
        'desconto',
        'estoque',
        'adicionado_em'
    ]

    list_editable = ['estoque']

    list_filter = ['categoria', EstoqueFiltro]

    search_fields = [
        'nome'
    ]

    list_per_page = 20

    list_select_related = ['categoria']

    actions = ['zerar_estoque']

    @admin.action(description="Zerar o estoque do produto selecionado")
    def zerar_estoque(self, request, queryset):
        updated = queryset.update(estoque=0)
        self.message_user(
            request,
            ngettext(
                "%d produto teve o estoque zerado com sucesso.",
                "%d produtos tiveram os estoques zerados com sucesso.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
        

