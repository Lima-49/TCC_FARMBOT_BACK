from flask import Flask, request, jsonify
from domain.iclient_arquivos import IClientesArquivosApp
from models.client_arquivos_model import ClientesDados


app = Flask(__name__)

icliente_arquivos = IClientesArquivosApp()
clientModel = ClientesDados()

@app.route('/files', methods=['POST'])
def add_new_file():
    data = request.json
    client_arquivos = ClientesDados(data['id_cliente'], data['descricao_arquivo'], data['url_bucket'], data['nome_arquivo'])
    result = icliente_arquivos.add_new_file(client_arquivos)
    return result

@app.route('/clients/<int:client_id>/files', methods=['GET'])
def get_client_files(client_id):
    result = icliente_arquivos.get_client_files(client_id)
    return result

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file_from_id(file_id):
    result = icliente_arquivos.get_file_from_id(file_id)
    return result

@app.route('/files/<int:file_id>', methods=['PUT'])
def update_file_from_id(file_id):
    data = request.json
    descricao_arquivo = data.get('descricao_arquivo')
    url_bucket = data.get('url_bucket')
    result = icliente_arquivos.update_file_from_id(file_id, descricao_arquivo, url_bucket)
    return result

@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file_from_id(file_id):
    result = icliente_arquivos.delete_file_from_id(file_id)
    return result

@app.route('/clients/<int:client_id>/upload-file', methods=['POST'])
def upload_file(client_id):
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    result = icliente_arquivos.add_file_from_request(client_id, file)
    return result
    
    