from src.models.models import User

def test_user_has_dict_attr(db_for_emprestimo):

    user = User.query.first()
    user_dict = user.to_dict()
    assert hasattr(user, 'to_dict')