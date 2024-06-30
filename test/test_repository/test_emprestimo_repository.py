import pytest
from unittest.mock import MagicMock

from src.repository.emprestimo.repository import EmprestimoRepository
from src.extensions.database.database import db

def test_create_emprestimo_rollback(mocker):
    # Crie uma instância do repositório
    repo = EmprestimoRepository(db)

    # Crie um mock para a sessão do banco de dados
    mock_session = mocker.patch.object(repo, 'db').session

    # Configure o mock do commit para lançar uma exceção
    mock_session.commit.side_effect = Exception("Database error")

    # Crie um objeto emprestimo de teste
    emprestimo = MagicMock()

    # Tente chamar o método create_emprestimo e verifique se ele lança a exceção
    with pytest.raises(Exception, match="Database error"):
        repo.create_emprestimo(emprestimo)

    # Verifique se o rollback foi chamado
    mock_session.rollback.assert_called_once()

    # Verifique se o emprestimo foi adicionado à sessão antes da exceção
    mock_session.add.assert_called_once_with(emprestimo)
