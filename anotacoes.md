# Ambiente Virtual com Poetry

Para ativar o ambiente virtual do Poetry, utilize o comando:

```bash
poetry shell
```

se nao ativar, use:
```bash
source $(poetry env info --path)/bin/activate
```

 Para sair do ambiente virtual, utilize o comando:
```bash
deactivate
```

## Gerenciamento de Dependências

Se for a primeira vez rodando o projeto, é necessário instalar as dependências. 

Para instalar dependências listadas no arquivo `pyproject.toml`, utilize o comando:
```bash
poetry install
```

Para adicionar uma nova dependência ao projeto, utilize o comando:
```bash
poetry add nome-da-dependencia
```

Para remover uma dependência do projeto, utilize o comando:
```bash
poetry remove nome-da-dependencia
```

Para atualizar todas as dependências do projeto, utilize o comando:
```bash
poetry update
```

Para listar as dependências instaladas no projeto, utilize o comando:
```bash
poetry show
```

Para verificar o status do ambiente virtual, utilize o comando:
```bash
poetry env info
```

# Criacao de um endpoint simples (apenas CRUD)

OBS: Considerando que a model ja esta criado

1. Primeiro crie o serializer no arquivo serializers.py
2. Depois crie a view no arquivo views.py ou crei um arquivo apenas para essa view e adicione o import no arquivo __init_.py
3. Por fim crie a rota no arquivo urls.py


# Principais Bibliotecas Utilizadas no Projeto

## Django REST Framework (DRF)
**Instalação:**
```bash
poetry add djangorestframework
```

**Configuração no settings.py:**
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]

```

**Para que serve:** Framework para criar APIs RESTful em Django. Facilita a criação de endpoints, serialização de dados, autenticação e permissões.

## Simple JWT (djangorestframework-simplejwt)
**Instalação:**
```bash
poetry add djangorestframework-simplejwt
```

**Configuração no settings.py:**
```python
from datetime import timedelta

INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),  # Token de acesso válido por 3 horas
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # Token de renovação válido por 1 dia
}
```

**Configuração no urls.py:**
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    ...
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**Para que serve:** Implementa autenticação JWT (JSON Web Tokens). Gera dois tokens:
- **Access Token**: usado em todas as requisições (válido por 3h)
- **Refresh Token**: usado para renovar o access token sem precisar fazer login novamente (válido por 1 dia)

**Como usar:**
1. Login: `POST /token/` com `{username, password}` → retorna `{access, refresh}`
2. Requisições: adicionar header `Authorization: Bearer <access_token>`
3. Renovar: `POST /token/refresh/` com `{refresh}` → retorna novo `{access}`

## DRF Spectacular
**Instalação:**
```bash
poetry add drf-spectacular
```

**Configuração no settings.py:**
```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Minha LivrariaAPI',
    'DESCRIPTION': 'API com os endpoints',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

**Configuração no urls.py:**
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

**Para que serve:** Gera documentação automática da API em formato OpenAPI 3. Disponibiliza interfaces interativas:
- **Swagger UI**: `/api/swagger/` - interface visual para testar endpoints
- **ReDoc**: `/api/redoc/` - documentação mais limpa e organizada
- **Schema JSON**: `/api/schema/` - especificação OpenAPI em JSON

## Django CORS Headers
**Instalação:**
```bash
poetry add django-cors-headers
```

**Configuração no settings.py:**
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Deve vir antes do CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    ...
]

# Exemplo de configuração (ajustar conforme necessário):
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue
]
# ou para desenvolvimento:
# CORS_ALLOW_ALL_ORIGINS = True
```

**Para que serve:** Permite que a API seja acessada por aplicações frontend rodando em domínios diferentes (resolve erro de CORS).

## WhiteNoise
**Instalação:**
```bash
poetry add whitenoise
```

**Configuração no settings.py:**
```python
MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

**Para que serve:** Serve arquivos estáticos (CSS, JS, imagens) de forma eficiente em produção, sem precisar de servidor web adicional como Nginx.

## Gunicorn
**Instalação:**
```bash
poetry add gunicorn
```

**Como usar em produção:**
```bash
gunicorn livraria.wsgi:application --bind 0.0.0.0:8000
```

**Para que serve:** Servidor WSGI para rodar aplicações Django em produção. Substitui o servidor de desenvolvimento do Django.

## Black (Formatação de Código)
**Instalação:**
```bash
poetry add black
```

**Como usar:**
```bash
black .
```

**Para que serve:** Formata automaticamente o código Python seguindo um padrão consistente.

---
