from pydantic import BaseModel
from typing import Optional, List

# --- USUÁRIO ---
# Base: Dados comuns (que tanto entram quanto saem)
class UsuarioBase(BaseModel):
    matricula: str
    email: str
    tipo_usuario: str

# Create: O que precisa para cadastrar (TEM senha)
class UsuarioCreate(UsuarioBase):
    senha: str

# Response: O que o sistema devolve (NÃO TEM senha, tem ID)
class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True

# --- LIVRO ---
class LivroCreate(BaseModel):
    isbn: str
    titulo: str
    autor: str
    genero: str

class Livro(LivroCreate):
    id: int
    class Config:
        from_attributes = True

# --- EXEMPLAR ---
class ExemplarCreate(BaseModel):
    livro_id: int
    star: int = 0
    
    

class Exemplar(ExemplarCreate):
    id_unico: int
    # Adicionamos o disponivel aqui para você ver se está na estante
    disponivel: bool = True 
    livro: Optional[Livro] = None
    class Config:
        from_attributes = True

# --- TROCA ---
class TrocaCreate(BaseModel):
    usuario_id: int
    exemplar_id: int

class Troca(TrocaCreate):
    id: int
    entrada: Optional[int] = None
    saida: Optional[int] = None
    class Config:
        from_attributes = True