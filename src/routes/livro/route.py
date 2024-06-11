from flask import Blueprint

livro = Blueprint("livro", __name__, url_prefix='/api/v1/')

@livro.get('livro')
def get_all_livros():
    from src.services.livro.service import book_service
    return book_service.get_all_livros()