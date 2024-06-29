from src.models.models import Funcionario

class FuncionarioRepository:
    def __init__(self, db):
        self.db = db

    def get_funcionario_by_id(self, funcionario_id: str):
        return Funcionario.query.filter_by(id=funcionario_id).first()