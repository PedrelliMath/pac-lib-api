from flask import Flask
from flask_cors import CORS
from src.extensions.database import database
from src.blueprints import blueprints
from src.extensions.database.database import db

from src.models.models import Livro, Autor, Editora, Exemplar, SituacaoExemplar, User, Emprestimo, Funcionario, Cadastro
from src.helpers.dateformats import calcular_data_devolucao

def create_app():
    app = Flask(__name__)
    CORS(app)
    blueprints.init_app(app)
    database.init_app(app)
    return app

def populate_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        funcionario = Funcionario(
            nome="John",
            sobrenome="Doe",
            cadastro=Cadastro(
                logradouro="Rua Exemplo",
                numero=123,
                complemento="Apto 101",
                bairro="Bairro Exemplo",
                UF="SP",
                email="john.doe@example.com",
                telefone="11999999999"
            )
        )

        # Create a new user (usuario)
        usuario = User(
            nome="Jane",
            sobrenome="Smith",
            cadastro=Cadastro(
                logradouro="Rua Exemplo",
                numero=456,
                complemento="Casa",
                bairro="Bairro Exemplo",
                UF="SP",
                email="jane.smith@example.com",
                telefone="11888888888"
            )
        )

        # Add and commit the funcionario and usuario
        db.session.add(funcionario)
        db.session.add(usuario)
        db.session.commit()

        # Create a new publisher (editora)
        editora = Editora(nome="Editora Exemplo")

        # Create new authors (autores)
        autor1 = Autor(nome="Autor 1")
        autor2 = Autor(nome="Autor 2")

        # Add and commit the editora and autores
        db.session.add(editora)
        db.session.add(autor1)
        db.session.add(autor2)
        db.session.commit()

        # Create new books (livros)
        livro1 = Livro(
            titulo="Livro 1",
            edicao=1,
            ISBN10="1234567890",
            ISBN13="123-1234567890",
            categoria="Ficção",
            ano_publicacao=2020,
            quantidade_exemplares=1,
            editora=editora,
            autores=[autor1, autor2]
        )

        livro2 = Livro(
            titulo="Livro 2",
            edicao=1,
            ISBN10="0987654321",
            ISBN13="123-0987654321",
            categoria="Aventura",
            ano_publicacao=2021,
            quantidade_exemplares=1,
            editora=editora,
            autores=[autor1]
        )

        livro3 = Livro(
            titulo="Livro 3",
            edicao=1,
            ISBN10="1122334455",
            ISBN13="123-1122334455",
            categoria="Romance",
            ano_publicacao=2022,
            quantidade_exemplares=1,
            editora=editora,
            autores=[autor2]
        )

        # Add and commit the livros
        db.session.add(livro1)
        db.session.add(livro2)
        db.session.add(livro3)
        db.session.commit()

        # Create new exemplares for the books
        exemplar1 = Exemplar(livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar2 = Exemplar(livro=livro2, situacao=SituacaoExemplar.EMPRESTADO)
        exemplar3 = Exemplar(livro=livro3, situacao=SituacaoExemplar.EMPRESTADO)
        exemplar4 = Exemplar(livro=livro1, situacao=SituacaoExemplar.EMPRESTADO)
        exemplar5 = Exemplar(livro=livro1, situacao=SituacaoExemplar.EMPRESTADO)
        exemplar6 = Exemplar(livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)

        # Create new emprestimos
        emprestimo1 = Emprestimo(
            usuario=usuario,
            funcionario=funcionario,
            data_devolucao=calcular_data_devolucao(),
            exemplares=[exemplar1]
        )

        emprestimo2 = Emprestimo(
            usuario=usuario,
            funcionario=funcionario,
            data_devolucao=calcular_data_devolucao(),
            exemplares=[exemplar2]
        )

        emprestimo3 = Emprestimo(
            usuario=usuario,
            funcionario=funcionario,
            data_devolucao=calcular_data_devolucao(),
            exemplares=[exemplar3]
        )

        # Add and commit the exemplares and emprestimos
        db.session.add(exemplar1)
        db.session.add(exemplar2)
        db.session.add(exemplar3)
        db.session.add(exemplar4)
        db.session.add(exemplar5)
        db.session.add(exemplar6)
        db.session.add(emprestimo1)
        db.session.add(emprestimo2)
        db.session.add(emprestimo3)
        db.session.commit()

        # Close the session
        db.session.close()

        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
    