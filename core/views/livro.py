from rest_framework.viewsets import ModelViewSet
from core.models import Livro
from core.serializer import LivroSerializer, LivroDetailSerializer

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    # serializer_class = LivroSerializer
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return LivroDetailSerializer # Maneira de apresentar os detalhes das chaves estrageiras
        return LivroSerializer