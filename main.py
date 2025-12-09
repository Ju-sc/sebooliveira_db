from typing import Union, List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from enum import Enum
import models, schemas, crud
from database import SessionLocal, engine

# Cria as tabelas se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SebOOLiveira API")

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. CRIAR AS OPÇÕES ---
class TipoUsuario(str, Enum):
    ALUNO = "Aluno"
    VOLUNTARIO = "Voluntário"

# --- 2. ROTA DE USUÁRIO ---
@app.post("/CadUser/")
def cadastrar_usuario(
    matricula: str, 
    email: str, 
    senha: str, 
    tipo: TipoUsuario, 
    db: Session = Depends(get_db)
):
    novo_usuario = schemas.UsuarioCreate(
        matricula=matricula, 
        email=email, 
        senha=senha, 
        tipo_usuario=tipo.value 
    )
    return crud.create_usuario(db=db, usuario=novo_usuario)

@app.get("/ListUsuarios/", response_model=List[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()   

# --- 3. LIVROS (ACERVO) ---
@app.post("/CadLivro/")
def cadastrar_livro(isbn: str, titulo: str, autor: str, genero: str, db: Session = Depends(get_db)):
    novo_livro = schemas.LivroCreate(
        isbn=isbn, titulo=titulo, autor=autor, genero=genero
    )
    return crud.create_livro(db=db, livro=novo_livro)

@app.get("/ListarLivros/", response_model=List[schemas.Livro])
def listar_todos_livros(db: Session = Depends(get_db)):
    return crud.get_livros(db)

# --- ROTA ATUALIZAR LIVRO (Usando ISBN para achar o livro) ---
@app.put("/AtualizarLivro/{isbn_original}")
def atualizar_livro(
    isbn_original: str, 
    novo_isbn: str = None,    # O "= None" torna opcional
    novo_titulo: str = None,  # O "= None" torna opcional
    novo_autor: str = None,   # O "= None" torna opcional
    novo_genero: str = None,  # O "= None" torna opcional
    db: Session = Depends(get_db)
):
    # Note que removemos o "schemas.LivroCreate" daqui, 
    # pois ele obrigaria a preencher tudo. Passamos os dados direto pro CRUD.
    
    resultado = crud.update_livro_por_isbn(
        db=db, 
        isbn_original=isbn_original, 
        novo_isbn=novo_isbn,
        novo_titulo=novo_titulo,
        novo_autor=novo_autor,
        novo_genero=novo_genero
    )
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Não encontrei nenhum livro com esse ISBN!")
    
    return {
        "mensagem": "Sucesso! O livro foi atualizado.",
        "livro_atualizado": resultado
    }

# --- EXEMPLARES ---
@app.post("/CadExemplar/")
def cadastrar_exemplar(
    isbn_do_livro: str,  # <--- MUDAMOS O NOME AQUI (Vai aparecer assim no Docs)
    estado_conservacao: int = 5, 
    db: Session = Depends(get_db)
):
    # 1. Agora usamos o novo nome para buscar no banco
    livro_pai = db.query(models.Livro).filter(models.Livro.isbn == isbn_do_livro).first()

    # 2. Segurança: Se o ISBN não existir, avisamos o erro
    if not livro_pai:
        raise HTTPException(status_code=404, detail="Não existe nenhum livro cadastrado com esse ISBN!")

    # 3. Cria o exemplar usando o ID do pai que encontramos
    novo_exemplar = schemas.ExemplarCreate(
        livro_id=livro_pai.id, 
        star=estado_conservacao
    )
    
    return crud.create_exemplar(db=db, exemplar=novo_exemplar)

@app.delete("/DelExemplar/")
def deletar_exemplar(
    id_do_exemplar: int, 
    db: Session = Depends(get_db)
):
    sucesso = crud.delete_exemplar(db=db, exemplar_id=id_do_exemplar)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail="Exemplar não encontrado! Verifique o ID.")
    
    return {"mensagem": f"O exemplar {id_do_exemplar} foi removido da estante."}

@app.get("/ListarExemplares/", response_model=List[schemas.Exemplar])
def listar_exemplares(db: Session = Depends(get_db)):
    # Usamos db.query direto aqui para não dar erro no crud
    return db.query(models.Exemplar).all()

# --- 5. TROCAS ---
@app.post("/RealizarTroca/")
def realizar_troca(
    id_usuario: int,         
    id_exemplar_entrou: int, 
    id_exemplar_saiu: int,   
    db: Session = Depends(get_db)
):
    # 1. Verifica se o livro que vai sair existe
    livro_saida = db.query(models.Exemplar).filter(models.Exemplar.id_unico == id_exemplar_saiu).first()
    
    if not livro_saida:
        raise HTTPException(status_code=404, detail="Livro de saída não encontrado no acervo!")
    
    if not livro_saida.disponivel:
        raise HTTPException(status_code=400, detail="Este livro já foi levado e não está na estante!")

    # 2. Registra a Troca
    nova_troca = models.Troca(
        usuario_id=id_usuario,
        exemplar_id=id_exemplar_saiu, 
        entrada=id_exemplar_entrou,   
        saida=id_exemplar_saiu        
    )
    db.add(nova_troca)

    # 3. Atualiza o status (Baixa no estoque)
    livro_saida.disponivel = False 
    
    # O livro que entrou fica disponível
    livro_entrada = db.query(models.Exemplar).filter(models.Exemplar.id_unico == id_exemplar_entrou).first()
    if livro_entrada:
        livro_entrada.disponivel = True

    db.commit()
    return {"mensagem": "Troca realizada com sucesso!", "status": "Estoque atualizado"}