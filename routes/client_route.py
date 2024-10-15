from flask import Blueprint, request
from domain.iclientes_app import IClientesApp
from models.client_model import Cliente
from models.login_model import Login

client_bp = Blueprint('client', __name__)

iclient_app = IClientesApp()
clientModel = Cliente()
loginModel = Login()

@client_bp.route('/clientes', methods=['POST'])
def create_new_client():
    data = request.json

    cliente = Cliente(data['nome'], data['sobrenome'], data['data_nascimento'], data['cpf'], data['email'], data['senha_login'])
    cliente.senha_login = loginModel.hash_senha(cliente.senha_login)
    
    result = iclient_app.create_new_client(cliente)
    return result

@client_bp.route('/clientes', methods=['GET'])
def get_all_clients():
    result = iclient_app.get_all_clients()
    return result

@client_bp.route('/clientes/<int:client_id>', methods=['GET'])
def get_cliente_by_id(client_id):
    result = iclient_app.get_client_by_id(client_id)
    return result

@client_bp.route('/clientes/<int:client_id>', methods=['PUT'])
def update_cliente_by_id(client_id):
    data = request.json
    cliente = Cliente(data['nome'], data['sobrenome'], data['data_nascimento'], data['cpf'], data['email'], data['senha_login'])
    result = iclient_app.update_client_by_id(client_id, cliente)
    return result

@client_bp.route('/clientes/<int:client_id>', methods=['DELETE'])
def delete_cliente_by_id(client_id):
    result = iclient_app.delete_client_by_id(client_id)
    return result

@client_bp.route('/clientes/auth', methods=['POST'])
def autentificar_login():
    
    data = request.json
    login = Login(data['email'], data['senha'])
    
    result = iclient_app.autentificar_login(login)
    return result