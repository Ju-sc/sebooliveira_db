from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo_usuario = Column(String(20), nullable=False)
    trocas = relationship("Troca", back_populates="usuario")

class Livro(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100))
    genero = Column(String(50))
    star = Column(Integer, default=0)
    exemplares = relationship("Exemplar", back_populates="livro")

class Exemplar(Base):
    __tablename__ = "exemplares"
    id_unico = Column(Integer, primary_key=True, index=True)
    star = Column(Integer, default=0)
    # Coluna nova para saber se está na estante
    disponivel = Column(Boolean, default=True) 
    livro_id = Column(Integer, ForeignKey("livros.id"))
    livro = relationship("Livro", back_populates="exemplares")
    trocas = relationship("Troca", back_populates="exemplar")

class Troca(Base):
    __tablename__ = "trocas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    exemplar_id = Column(Integer, ForeignKey("exemplares.id_unico"))
    entrada = Column(Integer, nullable=True)
    saida = Column(Integer, nullable=True)
    usuario = relationship("Usuario", back_populates="trocas")
    exemplar = relationship("Exemplar", back_populates="trocas")