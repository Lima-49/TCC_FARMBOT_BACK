from flask import Flask, request
from domain.iclientes_app import IClientesApp
from models.client_model import Cliente

app = Flask(__name__)

iclient_app = IClientesApp()
clientModel = Cliente()

@app.route('/clientes', methods=['POST'])
def create_new_client():
    data = request.json

    cliente = Cliente(data['nome'], data['sobrenome'], data['data_nascimento'], data['cpf'], data['email'], data['senha_login'])
    cliente.senha_login = clientModel.hash_senha(cliente.senha_login)
    
    result = iclient_app.create_new_client(cliente)
    return result

@app.route('/clientes', methods=['GET'])
def get_all_clients():
    result = iclient_app.get_all_clients()
    return result

@app.route('/clientes/<int:client_id>', methods=['GET'])
def get_cliente_by_id(client_id):
    result = iclient_app.get_client_by_id(client_id)
    return result

@app.route('/clientes/<int:client_id>', methods=['PUT'])
def update_cliente_by_id(client_id):
    data = request.json
    cliente = Cliente(data['nome'], data['sobrenome'], data['data_nascimento'], data['cpf'], data['email'], data['senha_login'])
    result = iclient_app.update_client_by_id(client_id, cliente)
    return result

@app.route('/clientes/<int:client_id>', methods=['DELETE'])
def delete_cliente_by_id(client_id):
    result = iclient_app.delete_client_by_id(client_id)
    return result

@app.route('/clientes/<client_email>', methods=['GET'])
def autentificar_login(client_email):
    result = iclient_app.get_client_by_email(client_email)
    return result