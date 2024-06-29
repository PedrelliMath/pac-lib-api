from src.models.models import Livro, Autor, Editora, Exemplar

class BookRepository:

    def __init__(self, db):
        self.db = db

    def get_all_livros(self):
        return Livro.query.all()
    
    def get_autor_by_name(self, autor_name: str):
        return Autor.query.filter_by(nome=autor_name).first()
    
    def get_editora_by_name(self, editora_name: str):
        return Editora.query.filter_by(nome=editora_name).first()
    
    def get_livro_by_titulo(self, livro_titulo: str):
        return Livro.query.filter_by(titulo=livro_titulo).first()
    
    def insert_autor(self, autor: Autor):
        try:
            self.db.session.add(autor)
            self.db.session.commit()
            return autor
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def insert_editora(self, editora: Editora):
        try:
            self.db.session.add(editora)
            self.db.session.commit()
            return editora
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def insert_exemplar(self, exemplar: Exemplar):
        try:
            self.db.session.add(exemplar)
            self.db.session.commit()
            return exemplar
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def insert_livro(self, livro: Livro):
        try:
            self.db.session.add(livro)
            self.db.session.commit()
            return livro
        except Exception as e:
            self.db.session.rollback()
            raise e
