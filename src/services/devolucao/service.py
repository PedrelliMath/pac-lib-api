from flask import jsonify, request

from src.models.models import Devolucao

from src.repository.devolucao.repository import DevolucaoRepository
from src.repository.exemplar.repository import ExemplarRepository
from src.repository.funcionario.repository import FuncionarioRepository
from src.repository.emprestimo.repository import EmprestimoRepository

class DevolucaoService:
    def __init__(
            self,
            devolucao_repository,
            exemplar_repository,
            funcionario_repository,
            emprestimo_repository
    ):
        self.devolucao_repository = devolucao_repository
        self.exemplar_repository = exemplar_repository
        self.funcionario_repository = funcionario_repository
        self.emprestimo_repository = emprestimo_repository

    def make_devolucao(self):
        devolucao_data = request.json

        funcionario_id = devolucao_data.get('funcionario_id')
        emprestimo_id = devolucao_data.get('emprestimo_id')

        if not emprestimo_id or not funcionario_id:
            return jsonify({'error':'Parametros invalidos no payload'}), 422
        
        try:
            emprestimo = self.emprestimo_repository.get_emprestimo_by_id(emprestimo_id)
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        if not emprestimo:
            return jsonify({'error':'Emprestimo not found'}), 404

        try:
            funcionario = self.funcionario_repository.get_funcionario_by_id(funcionario_id)
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        if not funcionario:
            return jsonify({'error':'Funcionario not found'}), 404
        
        if not emprestimo.status:
            return jsonify({'error':'Emprestimo ja finalizado'}), 409
        
        try:
            devolucao = Devolucao(
                funcionario_id=funcionario.id,
                emprestimo_id=emprestimo.id,
                emprestimo=emprestimo
            )
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        try:
            devolucao_db = self.devolucao_repository.make_devolucao(devolucao)
            if not devolucao_db:
                raise Exception
        except Exception as e:
            return jsonify({'error':'Internal Server Error'}), 500
        
        return jsonify({'data':devolucao_db.to_dict()}), 201
        
        
def create_devolucao_service():
    from src.extensions.database.database import db
    devolucao_repo = DevolucaoRepository(db)
    exemplar_repo = ExemplarRepository(db)
    funcionario_repo = FuncionarioRepository(db)
    emprestimo_repo = EmprestimoRepository(db)

    return DevolucaoService(
        devolucao_repository=devolucao_repo,
        exemplar_repository=exemplar_repo,
        funcionario_repository=funcionario_repo,
        emprestimo_repository=emprestimo_repo
    )

devolucao_service = create_devolucao_service()