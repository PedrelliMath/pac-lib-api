from src.routes.livro.route import livro
from src.routes.emprestimo.route import emprestimo
from src.routes.devolucao.route import devolucao

def init_app(app):
    app.register_blueprint(livro)
    app.register_blueprint(emprestimo)
    app.register_blueprint(devolucao)