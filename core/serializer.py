from rest_framework.serializers import ModelSerializer
from core.models import Categoria, Editora, Autor

# O serializer é um componente do Django Rest Framework que funciona como um tradutor bidirecional entre objetos Python (como modelos do Django) e formatos de dados como JSON
class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' # ou especifique os campos: ['id', 'descricao']

class EditoraSerializer(ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'