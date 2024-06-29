from src.models.models import Funcionario

def test_may_create_funcionario():

    funcionario_data = {
        'nome':'matheus',
        'sobrenome':'mauricio',
        'cadastro_id':1
    }

    funcionario = Funcionario(**funcionario_data)

    assert funcionario.nome == funcionario_data['nome']
    assert funcionario.sobrenome == funcionario_data['sobrenome']
    assert funcionario.cadastro_id == funcionario_data['cadastro_id']