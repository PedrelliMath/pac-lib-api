from src.models.models import User

class UsuarioRepository:
    def __init__(self, db):
        self.db = db
    
    def get_usuario_by_id(self, usuario_id: str):
        return User.query.filter_by(id=usuario_id).first()