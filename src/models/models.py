import datetime
import enum
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

from src.extensions.database.database import db
from src.helpers.dateformats import calcular_data_devolucao

class SituacaoExemplar(enum.Enum):
    DISPONIVEL = 'disponivel'
    EMPRESTADO = 'emprestado'

# Tabela associativa para relação muitos-para-muitos entre Livro e Autor
livro_autor = Table(
    'livro_autor', db.metadata,
    Column('livro_id', Integer, ForeignKey('livro.id')),
    Column('autor_id', Integer, ForeignKey('autor.id'))
)

# Tabela associativa para relação muitos-para-muitos entre Exemplar e Emprestimo
emprestimo_exemplar = Table(
    'emprestimo_exemplar', db.metadata,
    Column('exemplar_id', Integer, ForeignKey('exemplares.id')),
    Column('emprestimo_id', Integer, ForeignKey('emprestimo.id'))
)

# Classe base para herança
class BaseEntity(db.Model):
    __abstract__=True

    created_at = Column(DateTime, default=lambda: datetime.datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now(), nullable=False)

    def to_dict(self):
        return {
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# Classe Livro
class Livro(BaseEntity):
    __tablename__='livro'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(140), nullable=False)
    edicao = Column(Integer, nullable=False)
    ISBN10 = Column(String(10), nullable=True)
    ISBN13 = Column(String(14), nullable=True)
    categoria = Column(String(140), nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    quantidade_exemplares = Column(Integer, default=0)

    editora_id = Column(Integer, ForeignKey('editora.id'))
    editora = relationship("Editora", back_populates="livros")
    autores = relationship('Autor', secondary=livro_autor, back_populates='livros')
    exemplares = relationship('Exemplar', back_populates='livro')

    def to_dict(self):
        livro_dict = super().to_dict()
        livro_dict.update({
            'id': self.id,
            'titulo': self.titulo,
            'edicao': self.edicao,
            'ISBN10': self.ISBN10,
            'ISBN13': self.ISBN13,
            'categoria': self.categoria,
            'ano_publicacao': self.ano_publicacao,
            'quantidade_exemplares': self.quantidade_exemplares,
            'editora': {'id': self.editora.id, 'nome': self.editora.nome} if self.editora else None,
            'autores': [{'id': autor.id, 'nome': autor.nome} for autor in self.autores],
            'exemplares': [
                {
                    'id': exemplar.id,
                    'situacao': exemplar.situacao.value,
                } for exemplar in self.exemplares
            ]
        })
        return livro_dict

# Classe Autor
class Autor(BaseEntity):
    __tablename__='autor'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)

    livros = relationship('Livro', secondary=livro_autor, back_populates='autores')

    def to_dict(self):
        autor_dict = super().to_dict()
        autor_dict.update({
            'id': self.id,
            'nome': self.nome,
            'livros': [{'id': livro.id, 'titulo': livro.titulo} for livro in self.livros]
        })
        return autor_dict

# Classe Editora
class Editora(BaseEntity):
    __tablename__='editora'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)

    livros = relationship("Livro", back_populates="editora")

    def to_dict(self):
        editora_dict = super().to_dict()
        editora_dict.update({
            'id': self.id,
            'nome': self.nome,
            'livros': [{'id': livro.id, 'titulo': livro.titulo} for livro in self.livros]
        })
        return editora_dict

class Exemplar(BaseEntity):
    __tablename__='exemplares'

    id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
    livro_id = Column(Integer, ForeignKey('livro.id'))
    situacao = Column(Enum(SituacaoExemplar), nullable=False, default=SituacaoExemplar.DISPONIVEL)

    livro = relationship('Livro', back_populates='exemplares')
    emprestimo = relationship('Emprestimo', secondary=emprestimo_exemplar, back_populates='exemplares')

    def to_dict(self):
        exemplar_dict = super().to_dict()
        exemplar_dict.update({
            'id': self.id,
            'situacao': self.situacao.value,
            'emprestimo': self.emprestimo[0].to_dict() if self.situacao == SituacaoExemplar.EMPRESTADO and self.emprestimo else None
        })
        return exemplar_dict

class Emprestimo(BaseEntity):
    __tablename__='emprestimo'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'))
    data_devolucao = Column(DateTime, default=lambda: calcular_data_devolucao())
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))
    status = Column(Boolean, default=True)

    usuario = relationship('User')
    funcionario = relationship('Funcionario')
    exemplares = relationship('Exemplar', secondary=emprestimo_exemplar, back_populates='emprestimo')

    def to_dict(self):
        emprestimo_dict = super().to_dict()
        emprestimo_dict.update({
            'id': self.id,
            'user': {
                'id': self.usuario.id,
                'nome': self.usuario.nome,
                'sobrenome': self.usuario.sobrenome
            },
            'funcionario': {
                'id': self.funcionario.id,
                'nome': self.funcionario.nome,
                'sobrenome': self.funcionario.sobrenome
            },
            'exemplares':[{
                'id':exemplar.id
            }for exemplar in self.exemplares],
            'data_devolucao': self.data_devolucao.isoformat(),
            'status': self.atualiza_situacao()
        })
        return emprestimo_dict
    
    def atualiza_situacao(self):
        if self.status:
            current_date = datetime.datetime.now()
            return "Em andamento" if current_date <= self.data_devolucao else "Atrasado"
        return "Finalizado"

class Devolucao(BaseEntity):
    __tablename__='devolucao'

    id = Column(Integer, primary_key=True)
    emprestimo_id = Column(Integer, ForeignKey('emprestimo.id'))
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))

    emprestimo = relationship('Emprestimo')

    def to_dict(self):
        devolucao_dict = super().to_dict()
        devolucao_dict.update({
            'id':self.id,
            'emprestimo_id':self.emprestimo_id,
            'funcionario_id':self.funcionario_id
        })
        return devolucao_dict

class User(BaseEntity):
    __tablename__='usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    sobrenome = Column(String(140), nullable=False)
    cadastro_id = Column(Integer, ForeignKey('cadastro.id'))
    
    cadastro = relationship('Cadastro', back_populates='usuarios')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome
        }

class Funcionario(BaseEntity):
    __tablename__='funcionario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    sobrenome = Column(String(140), nullable=False)
    cadastro_id = Column(Integer, ForeignKey('cadastro.id'))

    cadastro = relationship('Cadastro', back_populates='funcionarios')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome
        }
    
class Cadastro(BaseEntity):
    __tablename__='cadastro'

    id = Column(Integer, primary_key=True)
    logradouro = Column(String(140), nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String(140), nullable=True)
    bairro = Column(String(140), nullable=False)
    UF = Column(String(2), nullable=False)
    email = Column(String(255), nullable=False)
    telefone = Column(String(13), nullable=False)
    
    usuarios = relationship('User', back_populates='cadastro')
    funcionarios = relationship('Funcionario', back_populates='cadastro')


