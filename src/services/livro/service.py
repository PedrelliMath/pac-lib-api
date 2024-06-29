from src.repository.livro.repository import BookRepository
from src.models.models import Livro, Editora, Autor, Exemplar, SituacaoExemplar

from flask import request, jsonify

import json

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def insert_livro(self):
        livro_data = request.json

        print(json.dumps(request.json))

        titulo = livro_data.get('titulo')
        autores = livro_data.get('autores')
        editora_nome = livro_data.get('editora')
        categoria = livro_data.get('categoria')
        edicao = livro_data.get('edicao')
        ano_publicacao = livro_data.get('ano_publicacao')
        codigo_exemplar = livro_data.get('codigo_exemplar')
        print(codigo_exemplar)

        if not titulo or not autores or not editora_nome or not categoria or not edicao or not ano_publicacao:
            return jsonify({'error': 'Parametros Invalidos no Payload'}), 422
        
        livro = self.book_repository.get_livro_by_titulo(titulo)

        if not livro:
            print(f'Livro "{titulo}" não encontrado, cadastrando livro...')

            
            editora = self.book_repository.get_editora_by_name(editora_nome)
            if not editora:
                print(f'Editora "{editora_nome}" não existe no banco, cadastrando...')

                editora = Editora(nome=editora_nome)
                try:
                    self.book_repository.insert_editora(editora)
                    print(f'Editora "{editora_nome}" cadastrada com sucesso.')
                except Exception as e:
                    print(f'Erro ao cadastrar editora "{editora_nome}": {str(e)}')
                    return jsonify({'error': f'Erro ao cadastrar editora "{editora_nome}"'}), 500

            autores_db = []
            for autor_name in autores:
                autor_db = self.book_repository.get_autor_by_name(autor_name)
                if not autor_db:
                    print(f'Autor "{autor_name}" não existe no banco, cadastrando...')
                    autor_db = Autor(nome=autor_name)
                    try:
                        self.book_repository.insert_autor(autor_db)
                        print(f'Autor "{autor_name}" cadastrado com sucesso.')
                    except Exception as e:
                        print(f'Erro ao cadastrar autor "{autor_name}": {str(e)}')
                        return jsonify({'error': f'Erro ao cadastrar autor "{autor_name}"'}), 500
                autores_db.append(autor_db)

            livro = Livro(
                titulo=titulo,
                autores=autores_db,
                editora=editora,
                categoria=categoria,
                edicao=edicao,
                ano_publicacao=ano_publicacao
            )

            try:
                livro = self.book_repository.insert_livro(livro)
                print(livro.to_dict())
                print(f'Livro "{livro.titulo}" cadastrado com sucesso.')
            except Exception as e:
                print(f'Erro ao cadastrar livro "{titulo}": {str(e)}')
                return jsonify({'error': f'Erro ao cadastrar livro "{titulo}"'}), 500

        exemplar = Exemplar(id=codigo_exemplar, livro=livro, situacao=SituacaoExemplar.DISPONIVEL)
        try:
            self.book_repository.insert_exemplar(exemplar)
            print(f'Exemplar do livro "{livro.titulo}" adicionado com sucesso.')
        except Exception as e:
            print(f'Erro ao cadastrar exemplar do livro "{livro.titulo}": {str(e)}')
            return jsonify({'error': f'Erro ao cadastrar exemplar do livro "{livro.titulo}"'}), 500

        return jsonify({'data': livro.to_dict()}), 201

    def get_all_livros(self):

        try:
            livros = self.book_repository.get_all_livros()
        except Exception as e:
            return jsonify({'error':f'Internal Server Error {e}'}), 500

        if not livros:  
            return jsonify({'error':'no books found'}), 404
        
        livros = [livro.to_dict() for livro in livros]

        return jsonify({'data':livros}), 200

from src.extensions.database.database import db
book_service = BookService(BookRepository(db))