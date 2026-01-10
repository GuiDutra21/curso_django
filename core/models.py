from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    descricao = models.CharField(max_length=255)
    
    def __str__(self):
        return self.descricao

class Editora(models.Model):
    nome = models.CharField(max_length=255)
    site = models.URLField()
    
    def __str__(self):
        return self.nome + f" ({self.site})" 

class Autor(models.Model):
    class Meta:
        verbose_name_plural = "autores" # Apenas para mudar o plural
        
    nome = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
    
class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    preco = models.FloatField()
    # O PROTECT funcina igual o RESTRICT do mySQL
    # Com o related_name podemos acessar todos os livros de uma categoria usando os comandos shell assim:
    # livros_da_categoria = categoria.livros.all()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="livros")
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT, related_name="livros")
    autores = models.ManyToManyField(Autor, related_name="livros")
    
    def __str__(self):
        return self.titulo + f" ({self.editora})"
    
class Compra(models.Model):
    
    # Isso eh igual a uma enum
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1,'Carrinho'
        REALIZADO = 2,'Realizado'
        PAGO = 3,'Pago'
        ENTREGUE = 4,'Entregue'
    
    usuario = models.ForeignKey(User,on_delete=models.PROTECT, related_name='compras')
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    
    def __str__(self):
        return f"{self.usuario} -- {self.get_status_display()}"

class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="+") # Esse + remove a possibilidade de acessar os itens a partir de livro
    quantidade = models.IntegerField()