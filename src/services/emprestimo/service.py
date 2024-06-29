from flask import jsonify, request

from src.helpers.dateformats import calcular_data_devolucao
from src.models.models import Emprestimo, SituacaoExemplar

from src.repository.emprestimo.repository import EmprestimoRepository
from src.repository.exemplar.repository import ExemplarRepository
from src.repository.funcionario.repository import FuncionarioRepository
from src.repository.usuario.repository import UsuarioRepository

class EmprestimoService:
    def __init__(
            self, 
            emprestimo_repository, 
            exemplar_repository,
            funcionario_repository,
            usuario_repository
    ):
        self.emprestimo_repository = emprestimo_repository
        self.exemplar_repository = exemplar_repository
        self.funcionario_repository = funcionario_repository
        self.usuario_repository = usuario_repository
    
    def create_emprestimo(self):
        emprestimo_data = request.json

        funcionario_id = emprestimo_data.get('funcionario_id')
        usuario_id = emprestimo_data.get('usuario_id')
        exemplar_id = emprestimo_data.get('exemplar_id')

        if not funcionario_id or not usuario_id or not exemplar_id:
            return jsonify({'error':'Parametros invalidos no payload'}), 422
        
        # Verifica se o exemplar existe e se está disponível
        exemplar = self.exemplar_repository.get_exemplar_by_id(exemplar_id)
        if not exemplar:
            return jsonify({'error':'Exemplar nao encontrado'}), 404
        
        if exemplar.situacao == SituacaoExemplar.EMPRESTADO:
            return jsonify({'error':'Exemplar ja emprestado'}), 409
        
        # Verifica se o funcionário existe
        funcionario = self.funcionario_repository.get_funcionario_by_id(funcionario_id)
        if not funcionario:
            return jsonify({'error':'Funcionario nao encontrado'}), 404
        
        # Verifica se o usuário existe
        usuario = self.usuario_repository.get_usuario_by_id(usuario_id)
        if not usuario:
            return jsonify({'error':'Usuario nao encontrado'}), 404
        
        # Cria o objeto Emprestimo
        emprestimo = Emprestimo(
            usuario=usuario,
            funcionario=funcionario,
            data_devolucao=calcular_data_devolucao(),
            exemplares=[exemplar]
        )

        try:
            emprestimo_db = self.emprestimo_repository.create_emprestimo(emprestimo)
        except Exception as e:
            return jsonify({'error':'Internal Server Error','message':str(e)}), 500
        
        return jsonify({'data':emprestimo_db.to_dict()}), 201
    
    def get_all_emprestimos(self):
        
        try:
            emprestimos_db = self.emprestimo_repository.get_all_emprestimos()
        except Exception as e:
            return jsonify({'error':'Internal Server Error','message':str(e)}), 500

        if not emprestimos_db:
            return jsonify({'error':'Emprestimos nao encontrados'}), 404
        
        emprestimo_dict = [emprestimo.to_dict() for emprestimo in emprestimos_db]

        return jsonify({'data':emprestimo_dict}), 200
    
def create_emprestimo_service():
    from src.extensions.database.database import db
    exemplar_repo = ExemplarRepository(db)
    emprestimo_repo = EmprestimoRepository(db)
    usuario_repo = UsuarioRepository(db)
    funcionario_repo = FuncionarioRepository(db)

    return EmprestimoService(
        emprestimo_repo, exemplar_repo, 
        funcionario_repo, usuario_repo
    )

emprestimo_service = create_emprestimo_service()
