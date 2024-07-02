from src.repository.livro.repository import BookRepository
from src.models.models import Livro, Editora, Autor, Exemplar, SituacaoExemplar

from flask import request, jsonify
from sqlalchemy import inspect

import json

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def insert_livro(self):
        livro_data = request.json

        titulo = livro_data.get('titulo')
        autores = livro_data.get('autores')
        editora_nome = livro_data.get('editora')
        categoria = livro_data.get('categoria')
        edicao = livro_data.get('edicao')
        ano_publicacao = livro_data.get('ano_publicacao')
        codigo_exemplar = livro_data.get('codigo_exemplar')

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
    
    def update_livro_by_id(self, livro_id):
        livro_data = request.json

        livro_columns = {c.key for c in inspect(Livro).mapper.column_attrs}
        invalid_keys = [key for key in livro_data.keys() if key not in livro_columns]

        if not livro_data:
            return jsonify({'error':'Parametros Invalidos no Payload'}), 422
        
        if invalid_keys:
            return jsonify({'error':f'{str(invalid_keys)} nao sao propriedades de livro'}), 422
        
        try:
            livro = self.book_repository.get_livro_by_id(livro_id)
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        if not livro:
            return jsonify({'error':'Livro not found'}), 404
        
        try:
            new_livro = self.book_repository.update_livro(livro, livro_data)
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        return jsonify({'data':new_livro.to_dict()})

    def delete_livro_by_id(self, livro_id):

        try:
            livro = self.book_repository.get_livro_by_id(livro_id)
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        if not livro:
            return jsonify({'error':'Livro not found'}), 404
        
        try:
            self.book_repository.delete_livro(livro)
        except Exception as e:
            return jsonify({'error':'Internal Server error'}), 500
        
        deleted_livro = self.book_repository.get_livro_by_id(livro_id)

        if deleted_livro:
            return jsonify({'error':'Internal Server Error'}), 500
        
        return jsonify({'data':'Livro deletado com sucesso'}), 200

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