from sqlalchemy import text

from src.app import create_app
from src.extensions.database.database import db
from src.models.models import Livro, Autor, Editora, Exemplar, SituacaoExemplar, User, Emprestimo, Funcionario, Cadastro
from src.helpers.dateformats import calcular_data_devolucao
from src.sql.triggers import incremente_exemplar, decrementa_exemplar

from datetime import datetime, timedelta

def populate_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()

        db.session.execute(text(incremente_exemplar))
        db.session.execute(text(decrementa_exemplar))
        
        funcionario1 = Funcionario(
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

        funcionario2 = Funcionario(
            nome="Matheus",
            sobrenome="Eduardo",
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
        usuario1 = User(
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

        usuario2 = User(
            nome="Pedrelli",
            sobrenome="Mauricio",
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
        db.session.add(funcionario1)
        db.session.add(funcionario2)
        db.session.add(usuario1)
        db.session.add(usuario2)
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
            quantidade_exemplares=0,
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
            quantidade_exemplares=0,
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
            quantidade_exemplares=0,
            editora=editora,
            autores=[autor2]
        )

        # Add and commit the livros
        db.session.add(livro1)
        db.session.add(livro2)
        db.session.add(livro3)
        db.session.commit()

        # Create new exemplares for the books
        exemplar1 = Exemplar(id='431', livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar2 = Exemplar(id='644', livro=livro2, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar3 = Exemplar(id='432', livro=livro3, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar4 = Exemplar(id='53534', livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar5 = Exemplar(id='404932', livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)
        exemplar6 = Exemplar(id='940530', livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)

        # Create new emprestimos
        emprestimo1 = Emprestimo(
            usuario=usuario1,
            funcionario=funcionario2,
            data_devolucao=datetime.now() - timedelta(days=1),
            exemplares=[exemplar1]
        )

        emprestimo2 = Emprestimo(
            usuario=usuario2,
            funcionario=funcionario1,
            data_devolucao=calcular_data_devolucao(),
            exemplares=[exemplar2]
        )

        emprestimo3 = Emprestimo(
            usuario=usuario2,
            funcionario=funcionario2,
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
        emprestimo1.exemplares[0].situacao = SituacaoExemplar.EMPRESTADO
        emprestimo2.exemplares[0].situacao = SituacaoExemplar.EMPRESTADO
        emprestimo3.exemplares[0].situacao = SituacaoExemplar.EMPRESTADO
        db.session.commit()


        # Close the session
        db.session.close()

        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()