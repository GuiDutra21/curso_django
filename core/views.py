import json
from django.http import HttpResponse,JsonResponse
from django.views import View
from core.models import Categoria
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def teste(request):
    return HttpResponse("ola mundo do django")

# csrf_exempt: Remove a verificação de token CSRF
# method_decorator: Adapta o decorator de função para funcionar em classes
# name="dispatch": Aplica o decorator no método dispatch() da classe, que processa todas as requisições (GET, POST, PUT, DELETE, etc.)


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
        
        

# Para fazer o retorno das resquisicoes eu posso usar tanto o HttpResponse quanto o JsonResponse, porem cada um tem os seus detalhes
