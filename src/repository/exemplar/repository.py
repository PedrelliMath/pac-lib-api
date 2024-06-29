from src.models.models import Exemplar

class ExemplarRepository:
    def __init__(self, db):
        self.db = db
    
    def get_exemplar_by_id(self, exemplar_id):
        return Exemplar.query.filter_by(id=exemplar_id).first()