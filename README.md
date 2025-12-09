# SebOOLiveira

 📚 SebOOLiveira API
Sistema de gerenciamento para Sebo/Biblioteca Escolar desenvolvido com FastAPI e MySQL. O projeto permite o cadastro de alunos, gerenciamento do acervo de livros, controle de exemplares físicos e realização de trocas de livros.

  🚀 Tecnologias Utilizadas
➣ Python 3.x
➣ FastAPI (Framework web moderno e rápido)
➣ SQLAlchemy (ORM para banco de dados)
➣ MySQL (Banco de dados relacional)
➣ Pydantic (Validação de dados)
➣ Uvicorn (Servidor ASGI)

⚙️ Funcionalidades
1. 👥 Usuários
  Cadastro de Alunos e Voluntários.
  Listagem de todos os usuários cadastrados.

3. 📖 Acervo (Livros Pai)
  Cadastro de obras literárias (Título, Autor, ISBN, Gênero).
  Atualização inteligente: Correção de dados do livro buscando pelo ISBN.
  Listagem do catálogo geral.

5. 🔖 Exemplares (Estoque Físico)
  Cadastro de exemplares físicos vinculados a um livro pai.
  Diferencial: Ao cadastrar, basta informar o ISBN do livro; o sistema localiza o ID automaticamente.
  Listagem detalhada (mostra os dados do livro pai dentro do exemplar).
  Remoção de exemplares da estante (Delete).

7. 🔄 Sistema de Trocas
  Realiza a troca de um livro por outro.
  Automação:
    O livro que sai (do acervo para o aluno) fica Indisponível.
    O livro que entra (do aluno para o acervo) fica Disponível.
    Registro histórico da transação na tabela de Trocas.

## 🛠️ Como Rodar o Projeto

* **➣ Pré-requisitos**
    * ➣ Python instalado.
    * ➣ MySQL Server rodando.
    * ➣ Um banco de dados criado (ex: `sebooliveira_db`).

* **➣ Passo a Passo**
    * **➣ Clone o repositório:**
        ```bash
        git clone [https://github.com/SeuUsuario/SebOOLiveira-API.git](https://github.com/SeuUsuario/SebOOLiveira-API.git)
        cd SebOOLiveira-API
        ```
    * **➣ Crie um ambiente virtual (Opcional, mas recomendado):**
        ```bash
        python -m venv venv
        # Windows:
        venv\Scripts\activate
        # Linux/Mac:
        source venv/bin/activate
        ```
    * **➣ Instale as dependências:**
        ```bash
        pip install -r requirements.txt
        ```
    * **➣ Configure o Banco de Dados:**
        * ➣ Abra o arquivo `database.py`.
        * ➣ Ajuste a linha `SQLALCHEMY_DATABASE_URL` com seu usuário e senha do MySQL:
            ```python
            "mysql+pymysql://SEU_USUARIO:SUA_SENHA@localhost:3306/NOME_DO_BANCO"
            ```
    * **➣ Rode o servidor:**
        ```bash
        uvicorn main:app --reload
        ```
    * **➣ Acesse a Documentação:**
        * ➣ Abra o navegador em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

🔌 Documentação das Rotas (Endpoints)

  ➣ Usuários
  
Método

Rota

Descrição


  ➣ POST
  
/CadUser/

Cria um novo usuário (Aluno ou Voluntário).


  ➣ GET
  
/ListUsuarios/

Lista todos os usuários.


  ➣ Livros (Acervo)
  
Método
Rota
Descrição


  ➣ POST
  
/CadLivro/

Cadastra um novo título no acervo.

  ➣ GET
  
/ListarLivros/

Lista todos os livros cadastrados.

  ➣ PUT
  
/AtualizarLivro/{isbn}

Atualiza dados de um livro buscando pelo ISBN. Campos são opcionais.


  ➣ Exemplares (Estoque)
Método

Rota

Descrição


  ➣ POST
  
/CadExemplar/

Cria uma cópia física. Usa o isbn_do_livro para vincular automaticamente.


  ➣ GET
  
/ListarExemplares/

Lista o estoque. Retorna o objeto livro aninhado.


  ➣ DELETE
  
/DelExemplar/

Remove um exemplar físico do banco de dados pelo ID.


  ➣ Trocas
  
Método

Rota

Descrição


  ➣ POST
  
/RealizarTroca/

Registra a troca, baixa o estoque de saída e disponibiliza a entrada.


📂 Estrutura do Projeto
main.py: Arquivo principal contendo todas as rotas da API.
models.py: Modelos das tabelas do banco de dados (SQLAlchemy).
schemas.py: Modelos de validação e serialização de dados (Pydantic).
crud.py: Funções que interagem diretamente com o banco (Create, Read, Update, Delete).
database.py: Configuração da conexão com o MySQL.

👨‍💻 Autores
Desenvolvido para o projeto SebOOLiveira por Jailine Coelho, Juliana Leite, Julio Da Cruz e Matheus Mafra.
                                      Focado em soluções simples e diretas.







