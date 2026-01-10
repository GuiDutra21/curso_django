from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.models import Categoria
from core.serializer import CategoriaSerializer

# Essas 2 classes abaixo foram feitas usando o Generic view
class CategoriasListGeneric(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriasDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'id' # Define qual campo do modelo será usado para buscar o objeto