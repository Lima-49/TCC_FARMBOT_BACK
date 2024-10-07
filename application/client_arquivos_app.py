from flask import jsonify
import pyodbc
from repository.client_arquivos_repository import ClientDadosRepository
from config import Config

class ClientesArquivos:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.connection_string
        self.repo = ClientDadosRepository(self.connection_string)

    def add_new_file(self, client_arquivo):
        try:
            self.repo.add_new_file(client_arquivo)
            return jsonify({'message': 'Arquivo salvo com sucesso!'}), 201
        
        except pyodbc.DatabaseError as df_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(df_err)}), 500
        
        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400
        
        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao adicionar um arquivo novo', 'details': str(e)}), 500
        
    def get_client_files(self, client_id):
        try:
            arquivos = self.repo.get_client_files(client_id)
            if arquivos:
                return jsonify(arquivos), 200
            else:
                return jsonify({'message': 'Nenhum arquivo encontrado para o cliente'}), 404
            
        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400

        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao obter os arquivos do cliente', 'details': str(e)}), 500
        
    def get_file_from_id(self, file_id):
        try:
            arquivo = self.repo.get_file_from_id(file_id)
            if arquivo:
                return jsonify(arquivo), 200
            else:
                return jsonify({'message': 'Arquivo não encontrado'}), 404
            
        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400

        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao obter o arquivo', 'details': str(e)}), 500
        
    def update_file_from_id(self, file_id, descricao_arquivo=None, url_bucket=None):
        try:
            self.repo.update_file_from_id(file_id, descricao_arquivo, url_bucket)
            return jsonify({'message': 'Arquivo atualizado com sucesso!'}), 200
            
        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400

        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao atualizar o arquivo', 'details': str(e)}), 500

    def delete_file_from_id(self, file_id):
        try:
            self.repo.delete_file_from_id(file_id)
            return jsonify({'message': 'Arquivo deletado com sucesso!'}), 200
            
        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400

        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao deletar o arquivo', 'details': str(e)}), 500


