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