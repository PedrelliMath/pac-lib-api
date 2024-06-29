from src.models.models import Cadastro

def test_may_create_cadastro():

    cadastro_data = {
        'logradouro':'Rua das flores',
        'numero':5,
        'complemento':'AP 14',
        'bairro':'Sitio-Cercado',
        'UF':'PR',
        'email':'lhr3@hotmail.com',
        'telefone':'041995773967'
    }

    cadastro = Cadastro(**cadastro_data)

    assert cadastro.logradouro == cadastro_data['logradouro']
    assert cadastro.numero == cadastro_data['numero']
    assert cadastro.complemento == cadastro_data['complemento']
    assert cadastro.bairro == cadastro_data['bairro']
    assert cadastro.UF == cadastro_data['UF']
    assert cadastro.email == cadastro_data['email']
    assert cadastro.telefone == cadastro_data['telefone']

