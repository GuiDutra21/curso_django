import json

from django.http import HttpResponse,JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from core.models import Categoria

def teste(request):
    return HttpResponse("ola mundo do django")

# csrf_exempt: Remove a verificação de token CSRF
# method_decorator: Adapta o decorator de função para funcionar em classes
# name="dispatch": Aplica o decorator no método dispatch() da classe, que processa todas as requisições (GET, POST, PUT, DELETE, etc.)

# O que ta nessa classe foi feito no padrao de Class-Based Views (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class CategoriaView(View):
    def get(self,request,id=None):
        
        # Retorna o elemento pelo id 
        if id:
            qs = Categoria.objects.get(id=id) # Recupera o elemento desejado
            data = {"id" : qs.id, "descricao": qs.descricao} # Cria o json que sera retornado
            
            # OBS: Outra maneira de criar o json:
            # data = {}
            # data['id'] = qs.id
            # data['descricao'] = qs.descricao
            
            return JsonResponse(data) # Retorna o elemento em Json
        else:
            data = list(Categoria.objects.values()) # recupera todas as categorias
            formatted_data = json.dumps(data, ensure_ascii = False) # Converte para Json
            return HttpResponse(formatted_data, content_type='application/json') # Retorna as categorias
    
    def post(self,request):
        json_data = json.loads(request.body) # Le a requisicao
        new_catagoria = Categoria.objects.create(**json_data) # Cria o objeto
        data = {"id" : new_catagoria.id, "descricao": new_catagoria.descricao} # Cria o json que sera retornado
        return JsonResponse(data)
    
    def patch(self, request, id):
        json_data = json.loads(request.body)
        qs = Categoria.objects.get(id=id)
        qs.descricao = json_data['descricao'] if 'descricao' in json_data else qs.descricao
        qs.save() # Com o save a mudança é gravada no banco de dados permanentemente
        data = {'id':qs.id, 'descricao': qs.descricao}
        return JsonResponse(data)
        
    def delete(self,request, id):
        qs = Categoria.objects.get(id=id)
        qs.delete()
        data = {'Mensagem' : 'Objeto deletado com sucesso'}
        return JsonResponse(data)
# Para fazer o retorno das resquisicoes eu posso usar tanto o HttpResponse quanto o JsonResponse, porem cada um tem os seus ajustes necessarios
        

# O serializer é um componente do Django Rest Framework que funciona como um tradutor bidirecional entre objetos Python (como modelos do Django) e formatos de dados como JSON
class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' # ou especifique os campos: ['id', 'descricao']

# O que ta nessas 2 classes abaixo foi feito usando o Django Rest Framework com o APIView
class CategoriasList(APIView):
    
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(seld,request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetail(APIView):
    
    def get(self,request,id):
        categorias = get_object_or_404(Categoria.objects.all(), id=id)
        serializer = CategoriaSerializer(categorias)
        return Response(serializer.data)
    
    def put(self,request,id):
        
        categoria = get_object_or_404(Categoria.objects.all(), id=id)
        serializer = CategoriaSerializer(categoria,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        categoria = get_object_or_404(Categoria.objects.all(), id=id)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Essas 2 classes abaixo foram feitas usando o Generic view
class CategoriasListGeneric(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriasDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'id' # Define qual campo do modelo será usado para buscar o objeto
    
# Essa classe foi feita usando o ModelViewSet
# Ao usar uma ViewSet eh recomendado usar o router
class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer