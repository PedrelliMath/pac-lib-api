from src.repository.livro.repository import BookRepository

from flask import jsonify

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book():
        pass
    
    def get_all_livros(self):

        try:
            livros = self.book_repository.get_all_livros()
        except Exception as e:
            return jsonify({'error':f'Internal Server Error {e}'}), 500

        if not livros:  
            return jsonify({'erro':'no books found'}), 404
        
        livros = [livro.to_dict() for livro in livros]

        return jsonify({'data':livros})

book_service = BookService(BookRepository())