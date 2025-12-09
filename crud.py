from sqlalchemy.orm import Session
import models, schemas

# --- USUÁRIOS ---
def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_user = models.Usuario(
        matricula=usuario.matricula,
        email=usuario.email,
        senha_hash=usuario.senha,
        tipo_usuario=usuario.tipo_usuario
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- LIVROS ---
def get_livros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Livro).offset(skip).limit(limit).all()

def create_livro(db: Session, livro: schemas.LivroCreate):
    db_livro = models.Livro(**livro.dict())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

# --- EXEMPLARES ---
def create_exemplar(db: Session, exemplar: schemas.ExemplarCreate):
    db_exemplar = models.Exemplar(**exemplar.dict())
    db.add(db_exemplar)
    db.commit()
    db.refresh(db_exemplar)
    return db_exemplar

def delete_exemplar(db: Session, exemplar_id: int):
    item = db.query(models.Exemplar).filter(models.Exemplar.id_unico == exemplar_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

# --- TROCAS ---
def create_troca(db: Session, troca: schemas.TrocaCreate):
    db_troca = models.Troca(**troca.dict())
    db.add(db_troca)
    db.commit()
    db.refresh(db_troca)
    return db_troca

# --- ATUALIZAR (Campos Opcionais) ---
def update_livro_por_isbn(
    db: Session, 
    isbn_original: str, 
    novo_isbn: str = None, 
    novo_titulo: str = None, 
    novo_autor: str = None, 
    novo_genero: str = None
):
    # 1. Busca o livro antigo
    livro_banco = db.query(models.Livro).filter(models.Livro.isbn == isbn_original).first()

    # 2. Se achou, atualiza SÓ O QUE FOI ENVIADO
    if livro_banco:
        if novo_isbn is not None:    # Só muda se você digitou algo novo
            livro_banco.isbn = novo_isbn
            
        if novo_titulo is not None:  # Só muda se você digitou algo novo
            livro_banco.titulo = novo_titulo
            
        if novo_autor is not None:   # Só muda se você digitou algo novo
            livro_banco.autor = novo_autor
            
        if novo_genero is not None:  # Só muda se você digitou algo novo
            livro_banco.genero = novo_genero
        
        db.commit()
        db.refresh(livro_banco)
        return livro_banco
    
    return None