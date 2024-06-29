def test_may_create_livro_and_return_201(client, create_and_drop_tables):
    livro_data = {
        'titulo': 'Livro das pedras',
        'autores': ['matheus', 'mauricio'],
        'edicao': 4,
        'editora': 'editora exemplo',
        'categoria': 'categoria das pedras',
        'ano_publicacao': 2024,
        'codigo_exemplar': 12345
    }

    response = client.post('api/v1/livro', json=livro_data)
    livro = response.json

    assert response.status_code == 201
    assert 'data' in livro.keys()

    data = livro['data']

    assert data['titulo'] == livro_data['titulo']
    assert data['edicao'] == livro_data['edicao']
    assert data['categoria'] == livro_data['categoria']
    assert data['ano_publicacao'] == livro_data['ano_publicacao']

    # Verificação dos autores
    expected_autores = set(livro_data['autores'])
    assert len(data['autores']) == len(expected_autores)
    for autor in data['autores']:
        assert autor['nome'] in expected_autores

    # Verificação da editora
    assert data['editora']['nome'] == livro_data['editora']

    # Verificação dos exemplares
    assert len(data['exemplares']) == 1
    exemplar = data['exemplares'][0]
    assert exemplar['id'] == livro_data['codigo_exemplar']
    assert exemplar['situacao'] == 'disponivel'

def test_may_not_create_livro_and_return_422(client, create_and_drop_tables):

    livro_data = {
        'titulo': 'Livro das pedras',
        'autores': ['matheus', 'mauricio'],
        'editora': 'editora exemplo',
        'categoria': 'categoria das pedras',
        'ano_publicacao': 2024,
        'codigo_exemplar': 12345
    }

    response = client.post('/api/v1/livro', json=livro_data)
    livro = response.json

    assert response.status_code == 422
    assert 'error' in livro.keys()
    assert livro['error'] == 'Parametros Invalidos no Payload'

def test_may_return_all_livros_and_return_200(client, db_for_livro):

    response = client.get('/api/v1/livro')
    livros = response.json

    assert response.status_code == 200
    assert 'data' in livros.keys()

def test_may_not_return_livros_and_return_404(client, create_and_drop_tables):

    response = client.get('/api/v1/livro')
    livros = response.json

    assert response.status_code == 404
    assert 'error' in livros.keys()