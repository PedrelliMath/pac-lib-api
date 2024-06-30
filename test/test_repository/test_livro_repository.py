import pytest
from unittest.mock import MagicMock

from src.repository.livro.repository import BookRepository
from src.extensions.database.database import db

@pytest.mark.parametrize(
    'method_name, param',
    [
        ('insert_autor', MagicMock()),
        ('insert_editora', MagicMock()),
        ('insert_exemplar', MagicMock()),
        ('insert_livro', MagicMock()),
    ]
)
def test_livro_repository_methods_rollback(mocker, method_name, param):
    # Crie uma instância do repositório
    repo = BookRepository(db)

    # Crie um mock para a sessão do banco de dados
    mock_session = mocker.patch.object(repo.db, 'session')

    # Configure o mock do commit para lançar uma exceção
    mock_session.commit.side_effect = Exception("Database error")

    # Obtenha o método a ser testado
    method = getattr(repo, method_name)

    # Tente chamar o método e verifique se ele lança a exceção
    with pytest.raises(Exception, match="Database error"):
        method(param)

    # Verifique se o rollback foi chamado
    mock_session.rollback.assert_called_once()

    # Verifique se o objeto foi adicionado à sessão antes da exceção
    mock_session.add.assert_called_once_with(param)
