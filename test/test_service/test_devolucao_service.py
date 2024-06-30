import pytest
from src.models.models import Devolucao, Emprestimo, SituacaoExemplar

def test_may_create_devolucao_and_return_201(client, db_for_emprestimo):
    # Dados para criar um empréstimo
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    # Dados para criar uma devolução
    devolucao_data = {
        'emprestimo_id': '1',
        'funcionario_id': '1'
    }

    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    # Verifica se o empréstimo foi criado
    emprestimo_db_1 = Emprestimo.query.filter_by(id=1).first()
    assert emprestimo_db_1 is not None
    assert emprestimo_db_1.exemplares[0].situacao == SituacaoExemplar.EMPRESTADO

    # Criar uma devolução
    response_2 = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response_2.json
    assert response_2.status_code == 201

    # Verificações

    # Verifica se a devolução foi registrada corretamente no banco de dados
    devolucao_db = Devolucao.query.first()
    assert devolucao_db is not None
    assert devolucao_db.emprestimo_id == 1 
    assert devolucao_db.funcionario_id == 1

    # Verifica se a situação do exemplar mudou para Disponível
    emprestimo_db_2 = Emprestimo.query.filter_by(id=1).first()
    assert emprestimo_db_2 is not None
    assert emprestimo_db_2.exemplares[0].situacao == SituacaoExemplar.DISPONIVEL

    # Verifica os campos específicos do JSON de resposta
    data = devolucao['data']
    assert 'id' in data.keys()
    assert 'emprestimo_id' in data.keys()
    assert 'funcionario_id' in data.keys()

    # Comparação dos valores dos campos
    assert data['id'] == devolucao_db.id
    assert data['emprestimo_id'] == devolucao_db.emprestimo_id
    assert data['funcionario_id'] == devolucao_db.funcionario_id

def test_may_not_create_devolucao_and_return_422(client, create_and_drop_tables):
    
    devolucao_data = {
        'emprestimo_id': '1',
    }

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 422
    assert 'error' in devolucao.keys()
    assert devolucao['error'] == 'Parametros invalidos no payload'


devolucao_data = {
    'emprestimo_id': '1',
    'funcionario_id': '1'
}

@pytest.mark.parametrize(
    'devolucao_data, erro, repository, method',
    [
        (
            devolucao_data,
            'Internal Server Error',
            'src.repository.emprestimo.repository.EmprestimoRepository', 
            'get_emprestimo_by_id'
        ),
        (
            devolucao_data,
            'Internal Server Error',
            'src.repository.funcionario.repository.FuncionarioRepository', 
            'get_funcionario_by_id'
        ),
        (
            devolucao_data,
            'Internal Server Error',
            'src.models.models.Devolucao', 
            '__init__'
        ),
        (
            devolucao_data,
            'Internal Server Error',
            'src.repository.devolucao.repository.DevolucaoRepository', 
            'make_devolucao'
        ),
    ]
)
def test_may_not_create_devolucao_and_return_500(
        client, mocker, db_for_emprestimo,
        repository, erro, method, devolucao_data
):
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    mocker.patch(
        f'{repository}.{method}', 
        side_effect=Exception('Database error')
    )

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 500
    assert 'error' in devolucao.keys()
    assert devolucao['error'] == erro


def test_may_not_create_devolucao_by_None_return_and_return_500(
        client, mocker, db_for_emprestimo
):
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    devolucao_data = {
        'emprestimo_id': '1',
        'funcionario_id': '1'
    }

    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    mocker.patch(
        f'src.repository.devolucao.repository.DevolucaoRepository.make_devolucao', 
        return_value=None
    )

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 500
    assert 'error' in devolucao.keys()
    assert devolucao['error'] == 'Internal Server Error'

    devolucao = Devolucao.query.all()
    assert len(devolucao) == 0

devolucao_data = {
    'emprestimo_id': '2',
    'funcionario_id': '1'
}
@pytest.mark.parametrize(
        'devolucao_data, erro',
        [
            (
                {
                    'emprestimo_id': '2',
                    'funcionario_id': '1'
                }, 
                'Emprestimo not found'
            ),
            (
                {
                    'emprestimo_id':'1',
                    'funcionario_id':'2'
                },
                'Funcionario not found'
            )
        ]
)
def test_may_not_create_devolucao_and_return_404(
    client, db_for_emprestimo,
    devolucao_data, erro
):
        
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 404
    assert 'error' in devolucao.keys()
    assert devolucao['error'] == erro

    devolucao = Devolucao.query.all()
    assert len(devolucao) == 0

def test_may_not_duplicate_devolucao_and_return_409(
    client, db_for_emprestimo,
):
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    devolucao_data = {
        'emprestimo_id': '1',
        'funcionario_id': '1'
    }
    
    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 201

    devolucao = Devolucao.query.all()
    assert len(devolucao) == 1

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 409

    assert 'error' in devolucao.keys()
    assert devolucao['error'] == 'Emprestimo ja finalizado'

    devolucao = Devolucao.query.all()
    assert len(devolucao) == 1

def test_may_create_devolucao_and_emprestimo_finalizado(
    client, db_for_emprestimo,
):
    emprestimo_data = {
        'exemplar_id': '123',
        'funcionario_id': '1',
        'usuario_id': '1'
    }

    devolucao_data = {
        'emprestimo_id': '1',
        'funcionario_id': '1'
    }
    
    # Criar um empréstimo
    response_1 = client.post('/api/v1/emprestimo', json=emprestimo_data)
    assert response_1.status_code == 201

    response = client.post('/api/v1/devolucao', json=devolucao_data)
    devolucao = response.json
    assert response.status_code == 201

    emprestimo = Emprestimo.query.first()
    emprestimo_dict = emprestimo.to_dict()

    assert emprestimo_dict['status'] == 'Finalizado'