from flask import Blueprint

livro = Blueprint("livro", __name__, url_prefix='/api/v1/')

@livro.get('livro')
def get_all_livros():
    from src.services.livro.service import book_service
    return book_service.get_all_livros()

@livro.post('livro')
def insert_livro():
    from src.services.livro.service import book_service
    return book_service.insert_livro()

@livro.put('livro/<int:id>')
def update_livro_by_id(id):
    from src.services.livro.service import book_service
    return book_service.update_livro_by_id(id)

@livro.delete('livro/<int:id>')
def delete_livro_by_id(id):
    from src.services.livro.service import book_service
    return book_service.delete_livro_by_id(id)