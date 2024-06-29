from src.models.models import Autor

def test_may_create_autor_matheus():
    autor = Autor(nome='matheus')
    assert autor.nome == 'matheus'