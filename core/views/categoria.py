from rest_framework.viewsets import ModelViewSet

from core.models import Categoria
from core.serializer import CategoriaSerializer

# Essa classe foi feita usando o ModelViewSet
# Ao usar uma ViewSet eh recomendado usar o router
class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer