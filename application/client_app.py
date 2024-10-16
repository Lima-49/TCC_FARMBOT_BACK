from flask import jsonify
import pyodbc
from repository.client_repository import ClienteRepository
from config import Config
from models.login_model import Login
class ClientApp:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.connection_string
        self.repo = ClienteRepository(self.connection_string)
        self.loginModel = Login()

    def create_new_client(self, client):
        try:
            self.repo.create_new_client(client)
            return jsonify({'message': 'Cliente criado com sucesso!'}), 201

        except pyodbc.DatabaseError as db_err:
            # Tratamento para erros relacionados ao banco de dados
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            # Tratamento para erros de programação SQL, como sintaxe ou parâmetros incorretos
            return jsonify({'error': 'Erro de programação no SQL.', 'details': str(prog_err)}), 400

        except Exception as e:
            # Tratamento geral para qualquer outro tipo de erro
            return jsonify({'error': 'Ocorreu um erro desconhecido ao criar o cliente.', 'details': str(e)}), 500
        
    def get_all_clients(self):
        try:
            clientes = self.repo.get_all_clients()
            return jsonify([vars(cliente) for cliente in clientes]), 200

        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except Exception as e:
            return jsonify({'error': 'Erro desconhecido ao buscar clientes.', 'details': str(e)}), 500


    def get_client_by_id(self, id_cliente):
        try:
            cliente = self.repo.get_client_by_id(id_cliente)
            if cliente:
                return jsonify(vars(cliente)), 200
            return jsonify({'message': 'Cliente não encontrado!'}), 404

        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except Exception as e:
            return jsonify({'error': 'Erro desconhecido ao buscar cliente.', 'details': str(e)}), 500


    def update_client_by_id(self, id_cliente, client):
        try:
            cliente_existente = self.repo.get_client_by_id(id_cliente)
            if not cliente_existente:
                return jsonify({'message': 'Cliente não encontrado!'}), 404
            
            self.repo.update_client_by_id(id_cliente, client)
            return jsonify({'message': 'Cliente atualizado com sucesso!'}), 200

        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except Exception as e:
            return jsonify({'error': 'Erro desconhecido ao atualizar cliente.', 'details': str(e)}), 500


    def delete_client_by_id(self, id_cliente):
        try:
            cliente_existente = self.repo.get_client_by_id(id_cliente)
            if not cliente_existente:
                return jsonify({'message': 'Cliente não encontrado!'}), 404
            
            self.repo.delete_client_by_id(id_cliente)
            return jsonify({'message': 'Cliente deletado com sucesso!'}), 200

        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except Exception as e:
            return jsonify({'error': 'Erro desconhecido ao deletar cliente.', 'details': str(e)}), 500
        
    def autentificar_login(self, login_obj):
        try:
            client = self.repo.get_client_by_email(login_obj.email)
            
            if client:
                senha_valida = self.loginModel.verificar_senha(login_obj.senha, client.senha_login)
                
                if senha_valida:
                    return jsonify(vars(client)), 200
                else:
                    return jsonify({'message': 'E-mail ou senha inválidos'}), 404
                
            return jsonify({'message': 'Cliente não encontrado!'}), 404

        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados.', 'details': str(db_err)}), 500

        except Exception as e:
            return jsonify({'error': 'Erro desconhecido ao buscar cliente.', 'details': str(e)}), 500