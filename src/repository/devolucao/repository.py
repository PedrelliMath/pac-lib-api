from src.models.models import Devolucao, SituacaoExemplar

class DevolucaoRepository:
    def __init__(self, db):
        self.db = db
    
    def make_devolucao(self, devolucao: Devolucao):
        try:
            self.db.session.add(devolucao)
            devolucao.emprestimo.exemplares[0].situacao = SituacaoExemplar.DISPONIVEL
            devolucao.emprestimo.status = False
            self.db.session.commit()
            return devolucao
        except Exception as e:
            self.db.session.rollback()
            raise e