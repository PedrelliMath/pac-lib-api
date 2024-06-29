import pytest

from src.app import create_app
from src.extensions.database.database import db
from src.models.models import Emprestimo, Exemplar, Funcionario, User, Livro, Autor, Editora, SituacaoExemplar, Cadastro
from src.helpers.dateformats import calcular_data_devolucao

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def create_and_drop_tables(app):
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture(scope='function')
def db_for_emprestimo(create_and_drop_tables, request):
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

    db.session.add(funcionario1)
    db.session.add(usuario1)
    db.session.commit()

    editora = Editora(nome="Editora Exemplo")

    autor1 = Autor(nome="Autor 1")

    db.session.add(editora)
    db.session.add(autor1)
    db.session.commit()

    livro1 = Livro(
        titulo="Livro 1",
        edicao=1,
        ISBN10="1234567890",
        ISBN13="123-1234567890",
        categoria="Ficção",
        ano_publicacao=2020,
        quantidade_exemplares=1,
        editora=editora,
        autores=[autor1]
    )

    db.session.add(livro1)
    db.session.commit()

    exemplar1 = Exemplar(id='123', livro=livro1, situacao=SituacaoExemplar.DISPONIVEL)

    db.session.add(exemplar1)
    db.session.commit()

    print('Criado registros para teste de emprestimo...')

    yield db

    # Se a exceção for esperada, não tente excluir os registros
    if not hasattr(request, 'param') or not request.param.get('test_exception', False):
        db.session.query(Funcionario).delete()
        db.session.query(User).delete()
        db.session.query(Editora).delete()
        db.session.query(Autor).delete()
        db.session.query(Livro).delete()
        db.session.query(Exemplar).delete()
        db.session.query(Emprestimo).delete()
        db.session.commit()
        print('Removido registros para teste de emprestimo...')

@pytest.fixture(scope='function')
def db_for_livro(create_and_drop_tables):
    
    editora = Editora(nome="Editora Exemplo")

    autor1 = Autor(nome="Autor 1")

    db.session.add(editora)
    db.session.add(autor1)
    db.session.commit()

    livro1 = Livro(
        titulo="Livro 1",
        edicao=1,
        ISBN10="1234567890",
        ISBN13="123-1234567890",
        categoria="Ficção",
        ano_publicacao=2020,
        quantidade_exemplares=1,
        editora=editora,
        autores=[autor1]
    )

    db.session.add(livro1)
    db.session.commit()

    yield db

    db.session.query(Editora).delete()
    db.session.query(Autor).delete()
    db.session.query(Livro).delete()
    db.session.commit()