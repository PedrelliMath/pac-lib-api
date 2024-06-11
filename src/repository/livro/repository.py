from src.models.models import Livro, Autor, Editora

class BookRepository:
    
    @staticmethod
    def get_all_livros():
        return Livro.query.all()