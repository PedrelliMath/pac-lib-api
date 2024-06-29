from src.models.models import Editora

def test_may_create_editora():

    editora_data = {
        'id':1,
        'nome':'editora exemplo'
    }

    editora = Editora(**editora_data)

    assert editora.id == editora_data['id']
    assert editora.nome == editora_data['nome']