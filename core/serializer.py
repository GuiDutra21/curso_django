from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models import Categoria, Editora, Autor, Livro, Compra, ItensCompra
from rest_framework import serializers

# O serializer é um componente do Django Rest Framework que funciona como um tradutor bidirecional entre objetos Python (como modelos do Django) e formatos de dados como JSON
class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' # ou especifique os campos: ['id', 'descricao']

class EditoraSerializer(ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

class EditoraNestedSerialzer(ModelSerializer):
    class Meta:
        model = Editora
        fields = ("nome", "site",)

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'
        
class LivroSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

# Uma das possiveis maneiras de mostrar os detalhes(campos) das chaves estrageiras
class LivroDetailSerializer(ModelSerializer): 
    categoria = CharField(source="categoria.descricao") # Maneira para retornar apenas um campo
    autores = SerializerMethodField() # Maneira para retornar apenas o que vem da funcao get_autores
    editora = EditoraNestedSerialzer() # Maneira de controlar o que eh retornado atraves do Serializer criado
    
    class Meta:
        model = Livro
        fields = '__all__'
        depth = 1
    
    def get_autores(self, instance):
        nomes_autores = []
        autores = instance.autores.get_queryset()
        for autor in autores:
            nomes_autores.append(autor.nome)
        return nomes_autores

class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()
    
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 2
    
    def get_total(self, instance):
        return instance.quantidade * instance.livro.preco
        
class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email")
    status = SerializerMethodField()
    itens = ItensCompraSerializer(many=True)
    
    class Meta:
        model = Compra
        fields = ("id", "status", "usuario", "itens", "total")
    
    def get_status(self, instance):
        return instance.get_status_display() # Funcao que converte o numero na opcao da enum que defini nas models

class CriarEditarItensCompraSerialzier(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")
        
class CriarEditarCompraSerializer(ModelSerializer):
    itens = CriarEditarItensCompraSerialzier(many=True)
    # Com isso nao precisa mais passar o usuario na requisicao, pois ele ja pega o usuario atual
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())  
    
    class Meta:
        model = Compra
        fields = ("id", "usuario","itens")
    
    # O create foi necessario, pois os dados de compra e itensCompra estao anininhados(Nested) 
    def create(self, validated_data):
        itens = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            ItensCompra.objects.create(compra=compra,**item)
        compra.save()
        return compra
    
    # Lembrano que o instance eh o objeto que ja existe no banco e sera atualizado
    def update(self,instance, validated_data):
        itens = validated_data.pop("itens") # Pega os itens dos dados validados (da requisicao)
        if(itens):
            instance.itens.all().delete() # Apaga os itens antigos que estavam no objeto
            for item in itens:
                ItensCompra.objects.create(compra=instance,**item) # Cria novos itens no objeto
            instance.save() # Salva a instância da compra (recalcula total, etc)
        return instance    