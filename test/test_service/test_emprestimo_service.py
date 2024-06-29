import pytest
from src.helpers.dateformats import calcular_data_devolucao
from src.models.models import Emprestimo

def test_may_create_emprestimo_and_return_201(client, db_for_emprestimo):
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    response = client.post('/api/v1/emprestimo', json=emprestimo_data)
    emprestimo = response.json

    assert response.status_code == 201
    assert 'data' in emprestimo.keys()

    data = emprestimo['data']

    assert data['id'] == 1

    #Verificação campos de User
    assert data['user']['id'] == 1
    assert data['user']['nome'] == 'Jane'
    assert data['user']['sobrenome'] == 'Smith'

    #Verificação campos de Funcionario
    assert data['funcionario']['id'] == 1
    assert data['funcionario']['nome'] == 'John'
    assert data['funcionario']['sobrenome'] == 'Doe'

    #Verficação campos de Exemplar
    assert data['exemplares'][0]['id'] == 123

    #Compara datas sem as horas
    assert data['data_devolucao'].split('T')[0] == str(calcular_data_devolucao()).split(' ')[0]
    assert data['status'] == 'Em andamento'

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 1

def test_may_not_create_emprestimo_and_return_409(client, db_for_emprestimo):
        
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    client.post('/api/v1/emprestimo', json=emprestimo_data)
    response = client.post('/api/v1/emprestimo', json=emprestimo_data)
    emprestimo = response.json

    assert response.status_code == 409
    assert 'error' in emprestimo.keys()
    assert emprestimo['error'] == 'Exemplar ja emprestado'

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 1

def test_may_not_create_emprestimo_and_return_422(client, db_for_emprestimo):

    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
    }

    response = client.post('/api/v1/emprestimo', json=emprestimo_data)
    emprestimo = response.json

    assert response.status_code == 422
    assert 'error' in emprestimo.keys()
    assert emprestimo['error'] == 'Parametros invalidos no payload'

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 0

@pytest.mark.parametrize(
        'emprestimo_data,erro',
        [
            ({
                'exemplar_id': '543',
                'funcionario_id': '1',
                'usuario_id': '1'
            },'Exemplar nao encontrado'),
            ({
                'exemplar_id': '123',
                'funcionario_id': '2',
                'usuario_id': '1'
            },'Funcionario nao encontrado'),
            ({
                'exemplar_id': '123',
                'funcionario_id': '1',
                'usuario_id': '2'
            },'Usuario nao encontrado')
        ]
    )
def test_may_not_create_emprestimo_and_return_404(client, db_for_emprestimo, emprestimo_data, erro):

    response = client.post('/api/v1/emprestimo', json=emprestimo_data)
    emprestimo = response.json

    assert response.status_code == 404
    assert 'error' in emprestimo.keys()
    assert emprestimo['error'] == erro

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 0

def test_may_not_return_emprestimos_and_return_404(client, create_and_drop_tables):

    response = client.get('/api/v1/emprestimo')
    emprestimo = response.json

    assert response.status_code == 404
    assert 'error' in emprestimo.keys()
    assert emprestimo['error'] == 'Emprestimos nao encontrados'

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 0

def test_may_return_emprestimos_and_return_200(client, db_for_emprestimo):

    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    client.post('/api/v1/emprestimo', json=emprestimo_data)
    response = client.get('/api/v1/emprestimo')

    emprestimo = response.json

    assert response.status_code == 200
    assert 'data' in emprestimo.keys()

    emprestimo_db = Emprestimo.query.all()
    assert len(emprestimo_db) == 1


@pytest.mark.parametrize('db_for_emprestimo', [{'test_exception': True}], indirect=True)
def test_may_not_create_emprestimo_and_return_500(client, mocker, db_for_emprestimo):
    # Dados para criar um empréstimo
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    # Simula uma exceção durante a criação do empréstimo
    mocker.patch(
        'src.repository.emprestimo.repository.EmprestimoRepository.create_emprestimo', 
        side_effect=Exception('Database error')
    )

    # Faz uma requisição POST para criar o empréstimo
    response = client.post('/api/v1/emprestimo', json=emprestimo_data)

    # Verifica a resposta
    assert response.status_code == 500
    response_data = response.json
    assert 'error' in response_data
    assert response_data['error'] == 'Internal Server Error'
    assert 'message' in response_data
    assert response_data['message'] == 'Database error'

@pytest.mark.parametrize('db_for_emprestimo', [{'test_exception': True}], indirect=True)
def test_may_not_return_emprestimos_and_return_500(client, mocker, db_for_emprestimo):
    # Simula uma exceção durante a obtenção de todos os empréstimos
    mocker.patch(
        'src.repository.emprestimo.repository.EmprestimoRepository.get_all_emprestimos', 
        side_effect=Exception('Database error')
    )

    # Faz uma requisição GET para obter todos os empréstimos
    response = client.get('/api/v1/emprestimo')

    # Verifica a resposta
    assert response.status_code == 500
    response_data = response.json
    assert 'error' in response_data
    assert response_data['error'] == 'Internal Server Error'
    assert 'message' in response_data
    assert response_data['message'] == 'Database error'