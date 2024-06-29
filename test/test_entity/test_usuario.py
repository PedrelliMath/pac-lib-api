from src.models.models import User

def test_may_create_usuario():

    usuario_data = {
        'nome':'matheus',
        'sobrenome':'mauricio',
        'cadastro_id':1
    }

    usuario = User(**usuario_data)

    assert usuario.nome == usuario_data['nome']
    assert usuario.sobrenome == usuario_data['sobrenome']
    assert usuario.cadastro_id == usuario_data['cadastro_id']