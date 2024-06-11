from src.routes.livro.route import livro

def init_app(app):
    app.register_blueprint(livro)