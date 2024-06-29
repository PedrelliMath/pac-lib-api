from src.models.models import Emprestimo

def test_may_create_emprestimo():

    emprestimo_data = {
        'id':1,
        'user_id':1,
        'funcionario_id':1,
    }

    emprestimo = Emprestimo(**emprestimo_data)

    assert emprestimo.id == emprestimo_data['id']
    assert emprestimo.user_id == emprestimo_data['user_id']
    assert emprestimo.funcionario_id == emprestimo_data['funcionario_id']