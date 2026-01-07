from django.contrib import admin

# Register your models here

from core.models import Autor, Categoria, Compra, Editora, Livro, ItensCompra

admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Editora)
admin.site.register(Livro)

# Isso aqui permite adicionar/editar múltiplos ItensCompra diretamente na tela de edição da Compra na interface do Django
class ItensInline(admin.TabularInline):
    model = ItensCompra
    
@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    inlines = (ItensInline,)