from src.models.models import Emprestimo, SituacaoExemplar

class EmprestimoRepository:
    def __init__(self, db):
        self.db = db
    
    def create_emprestimo(self, emprestimo: Emprestimo):
        try:
            self.db.session.add(emprestimo)
            emprestimo.exemplares[0].situacao = SituacaoExemplar.EMPRESTADO
            self.db.session.commit()
            return emprestimo
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def get_all_emprestimos(self):
        return Emprestimo.query.all()
    
    def get_emprestimo_by_id(self, emprestimo_id: str):
        return Emprestimo.query.filter_by(id=emprestimo_id).first()