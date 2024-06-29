from flask import Blueprint

devolucao = Blueprint("devolucao", __name__, url_prefix='/api/v1/')

@devolucao.post('/devolucao')
def make_devolucao():
    from src.services.devolucao.service import devolucao_service
    return devolucao_service.make_devolucao()