from flask import jsonify
import pyodbc
from config import Config
from repository.configuracoes_tarefa_repository import ConfiguracoesTarefasRepository

class ConfiguracoesTarefaApp:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.connection_string
        self.repo = ConfiguracoesTarefasRepository(self.connection_string)
        
    def add_new_file(self, config_tarefa):
        try:
            self.repo.add_new_config_job(config_tarefa)
            return jsonify({'message': 'Configuração salva com sucesso!'}), 201
        except pyodbc.DatabaseError as df_err:
                return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(df_err)}), 500
                
        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400
        
        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao adicionar um arquivo novo', 'details': str(e)}), 500

    def get_config_jobs(self, client_id):
        try:
            configs = self.repo.get_config_jobs(client_id)
            
            if configs:
                return jsonify(configs), 200
            else:
                return jsonify({'message': 'Nenhuma configuracao encontrada para o cliente'}), 404
        except pyodbc.DatabaseError as db_err:
            return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(db_err)}), 500

        except pyodbc.ProgrammingError as prog_err:
            return jsonify({'error': 'Erro de programação no SQL', 'details': str(prog_err)}), 400

        except Exception as e:
            return jsonify({'error': 'Ocorreu um erro desconhecido ao obter os arquivos do cliente', 'details': str(e)}), 500
        