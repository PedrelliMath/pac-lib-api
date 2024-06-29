from src.models.models import Exemplar, SituacaoExemplar

def test_may_create_exemplar():

    exemplar_data = {
        'id':1,
        'livro_id':4,
        'situacao':SituacaoExemplar.DISPONIVEL
    }

    exemplar = Exemplar(**exemplar_data)

    assert exemplar.id == exemplar_data['id']
    assert exemplar.livro_id == exemplar_data['livro_id']
    assert exemplar.situacao == exemplar_data['situacao']