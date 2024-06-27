# MercadoLivre SDK
Este SDK oferece uma interface para gerenciar produtos na plataforma MercadoLivre usando Python.

## Funcionalidades
- Gerenciamento de produtos Criação, 
- atualização e exclusão de produtos 
- Fechamento de produtos
- Obtenção e atualização de descrições de produtos
## Instalação
Para instalar o SDK, use pip:

```bash

pip install mercadolivresdk
```
## Uso
```python
from mercadolivresdk.manager.product import ProductManager
from mercadolivresdk.models.product import ProductCreate, ProductUpdate, ProductDescription

# Inicialize o gerenciador de produtos
pm = ProductManager(access_token='seu_access_token')

# Exemplo de obtenção de um produto
product = pm.get_product(product_id='123456')
print(product)

# Exemplo de criação de um produto
new_product = ProductCreate(...)
created_product = pm.create_product(new_product)
print(created_product)

# Exemplo de atualização de um produto
updated_product = ProductUpdate(...)
pm.update_product(product_id='123456', product=updated_product)

# Exemplo de fechamento de um produto
pm.close_product(product_id='123456')

# Exemplo de exclusão de um produto
pm.delete_product(product_id='123456')

# Exemplo de obtenção da descrição de um produto
description = pm.get_product_description(product_id='123456')
print(description)

# Exemplo de atualização da descrição de um produto
new_description = ProductDescription(...)
pm.update_product_description(product_id='123456', description=new_description)
```

## Estrutura do Projeto
```markdown
mercadolivresdk/
│
├── internal/
│   └── manager/
│       └── product.py
├── models/
│   ├── __init__.py
│   └── product.py
├── tests/
│   ├── __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

## Contribuindo
Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato
Para quaisquer dúvidas, por favor, abra uma issue neste repositório.

