from src.models.models import Devolucao

def test_may_create_devolucao():

    devolucao_data = {
        'id':1,
        'emprestimo_id':1,
        'funcionario_id':1
    }

    devolucao = Devolucao(**devolucao_data)

    assert devolucao.id == devolucao_data['id']
    assert devolucao.emprestimo_id == devolucao_data['emprestimo_id']
    assert devolucao.funcionario_id == devolucao_data['funcionario_id']