# Intelli-Patinex

## Sobre o Projeto
O Intelli-Patinex é uma aplicação web desenvolvida em Django para gerenciamento e análise de planilhas. O sistema oferece funcionalidades para autenticação de usuários e manipulação de arquivos Excel, proporcionando uma interface intuitiva para processamento de dados.

## Tecnologias Utilizadas
- Python 3.x
- Django 3.2+
- Pandas 1.3+
- OpenPyXL 3.0.7+
- Django Crispy Forms
- Crispy Bootstrap 5
- SQLite (Banco de dados padrão)

## Estrutura do Projeto
```
intelli-patinex/
├── authentication/      # Aplicação de autenticação
├── sheets_app/          # Aplicação principal para manipulação de planilhas
├── intelli_patinex/     # Configurações principais do projeto
├── media/               # Diretório para arquivos de mídia
├── venv/                # Ambiente virtual Python
├── manage.py            # Script de gerenciamento Django
└── requirements.txt     # Dependências do projeto
```

## Pré-requisitos
- Python 3.x
- Pip (Gerenciador de pacotes Python)
- Ambiente virtual Python (recomendado)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/jvitor-gomes/intelli-patinex
cd intelli-patinex
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

5. Crie um superusuário (opcional):
```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

O projeto estará disponível em `http://localhost:8000`

## Funcionalidades Principais
- Sistema de autenticação de usuários
- Upload e processamento de planilhas Excel
- Interface intuitiva com Bootstrap 5
- Gerenciamento de arquivos

## Contato

[![linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white/)](https://www.linkedin.com/in/joaovitorgomesbastosdossantos/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:bgomes.joaovitor@gmail.com)
[![Portfólio](https://img.shields.io/badge/Portfólio-Visitar-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jvitor-gomes)