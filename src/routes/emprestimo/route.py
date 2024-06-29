from flask import Blueprint

emprestimo = Blueprint("emprestimo", __name__, url_prefix='/api/v1/')

@emprestimo.post('/emprestimo')
def create_emprestimo():
    from src.services.emprestimo.service import emprestimo_service
    return emprestimo_service.create_emprestimo()

@emprestimo.get('/emprestimo')
def get_all_emprestimos():
    from src.services.emprestimo.service import emprestimo_service
    return emprestimo_service.get_all_emprestimos()