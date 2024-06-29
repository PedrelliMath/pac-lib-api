from src.models.models import Livro

def test_may_create_livro():

    livro_data = {
        'titulo':'Livro das pedras',
        'edicao':4,
        'ISBN10':'1234567890',
        'ISBN13':'1234567890123',
        'categoria':'categoria das pedras',
        'ano_publicacao':2
    }

    livro = Livro(**livro_data)

    assert livro.titulo == livro_data['titulo']
    assert livro.edicao == livro_data['edicao']
    assert livro.ISBN10 == livro_data['ISBN10']
    assert livro.ISBN13 == livro_data['ISBN13']
    assert livro.categoria == livro_data['categoria']
    assert livro.ano_publicacao == livro_data['ano_publicacao']