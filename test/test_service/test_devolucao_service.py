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
