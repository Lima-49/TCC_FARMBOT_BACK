from flask import Flask
from routes.client_route import client_bp
from routes.client_arquivos_route import client_arquivos_bp
from routes.configuracoes_tarefas_route import config_tarefa_bp

app = Flask(__name__)

# Registrar os blueprints
app.register_blueprint(client_bp)
app.register_blueprint(client_arquivos_bp)
app.register_blueprint(config_tarefa_bp)

if __name__ == '__main__':
    app.run(debug=True)
