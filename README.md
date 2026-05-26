# API Gerenciador de Tarefas 🚀

Este projeto utiliza o **Poetry** para o gerenciamento de dependências e ambiente virtual.

## 🛠️ Como instalar e rodar o projeto

Siga os passos abaixo para configurar o ambiente local após clonar o repositório.

### 1. Pré-requisitos
Certifique-se de ter o Python (versão 3.10 ou superior) e o Poetry instalados na sua máquina.
Se não tiver o Poetry, instale com:
```bash
pip install poetry
```

### 2. Instalar as Dependências
Navegue até a pasta do projeto e execute o comando abaixo. Ele criará o ambiente virtual automaticamente e instalará todas as dependências registradas no arquivo `poetry.lock`:
```bash
poetry install
```

### 3. Ativar o Ambiente Virtual (Opcional)
Para entrar dentro do ambiente isolado criado pelo Poetry:
```bash
poetry shell
```

### 4. Executar o Projeto
*(Ajuste o comando abaixo de acordo com o framework da sua API, ex: FastAPI/Uvicorn, Flask ou Django)*
```bash
poetry run uvicorn main:app --reload
```
