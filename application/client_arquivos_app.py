from flask import jsonify
import pyodbc
from repository.client_arquivos_repository import ClientDadosRepository
from config import Config
from google.cloud import storage
import pandas as pd

class ClientesArquivos:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.connection_string
        self.repo = ClientDadosRepository(self.connection_string)
        self.bucket_name = self.config.bucket_name

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

    def upload_file_to_gcp(self, file, file_name):
        storage_client = storage.Client.from_service_account_json(self.config.credentials_path)
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_file(file)
        return blob.public_url.replace("googleapis", "cloud.google")
    
    def download_file_from_gcp(self, blob_name):
        storage_client = storage.Client.from_service_account_json(self.config.credentials_path)
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        data_file = blob.download_as_bytes()
        df = pd.read_excel(data_file)
        
        return df
            
    def add_file_from_request(self, client_id, file):
        
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo inválido'}), 400
        
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            try:
                file_name = f"{client_id}/{file.filename}"
                file_url = self.upload_file_to_gcp(file, file_name)
                return jsonify({'message': 'Arquivo salvo com sucesso!', 'url': file_url}), 200
            except Exception as e:
                return jsonify({'error': 'Erro ao fazer o upload', 'details': str(e)}), 500
        else:
            return jsonify({'error': 'Formato de arquivo não suportado. Envie um CSV ou Excel'}), 400
        
    def return_file_as_json(self, client_id, tipo_arquivo):
        try:
            data = self.repo.get_client_files(client_id)
            
            df = pd.DataFrame(data)
            df_filt = df[df['tipo_arquivo']==tipo_arquivo]
            
            blob_name = str(client_id) + "/" + str(df_filt['nome_arquivo'].iloc[0])
            df_client = self.download_file_from_gcp(blob_name)

            dict_df = {col: df_client[col].tolist() for col in df_client.columns}

            return jsonify(dict_df), 200
        except Exception as e:
            return jsonify({'message': 'Ocorreu um erro', 'details': str(e)}), 500
