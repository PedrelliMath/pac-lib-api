from src.models.models import Funcionario

def test_user_has_dict_attr(db_for_emprestimo):

    funcionario = Funcionario.query.first()
    funcionario_dict = funcionario.to_dict()
    assert hasattr(funcionario, 'to_dict')