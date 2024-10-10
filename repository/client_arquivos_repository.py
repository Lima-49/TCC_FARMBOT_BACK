import pyodbc
from models.client_arquivos_model import ClientesDados

class ClientDadosRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def connect(self):
        return pyodbc.connect(self.connection_string)
    
    def add_new_file(self, client_data):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO CLIENTES_ARQUIVOS (ID_CLIENTE, DESCRICAO_ARQUIVO, URL_BUCKET, NOME_ARQUIVO)
                VALUES (?, ?, ?, ?)
                """, (client_data.id_cliente, client_data.descricao_arquivo, client_data.url_bucket, client_data.nome_arquivo)
            )
            conn.commit()
            
    def get_client_files(self, client_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    ID_ARQUIVO AS id_arquivo,
                    ID_CLIENTE AS id_cliente,
                    DESCRICAO_ARQUIVO AS descricao_arquivo,
                    URL_BUCKET AS url_bucket,
                    NOME_ARQUIVO AS nome_arquivo
                FROM 
                    CLIENTES_ARQUIVOS
                WHERE
                    CLIENT_ID = ?
                """,(client_id)
            )
            
            arquivos = []
            
            for row in cursor.fetchall():
                client_data = {
                    'id_arquivo': row[0],
                    'id_cliente': row[1],
                    'descricao_arquivo': row[2],
                    'url_bucket': row[3],
                    'nome_arquivo': row[4]
                }
                
                clientes_arquivos = ClientesDados.from_dict(client_data)
                arquivos.append(client_data)
            
            return clientes_arquivos
        
    def get_file_from_id(self, file_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    ID_ARQUIVO AS id_arquivo,
                    ID_CLIENTE AS id_cliente,
                    DESCRICAO_ARQUIVO AS descricao_arquivo,
                    URL_BUCKET AS url_bucket,
                    NOME_ARQUIVO AS nome_arquivo
                FROM 
                    CLIENTES_ARQUIVOS
                WHERE
                    ID_ARQUIVO = ?
                """, (file_id,)
            )
            
            row = cursor.fetchone()
            if row:
                client_data = {
                    'id_arquivo': row[0],
                    'id_cliente': row[1],
                    'descricao_arquivo': row[2],
                    'url_bucket': row[3],
                    'nome_arquivo': row[4]
                }
                return ClientesDados.from_dict(client_data)
            return None

    def update_file_from_id(self, file_id, descricao_arquivo=None, url_bucket=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            query = """
                UPDATE CLIENTES_ARQUIVOS
                SET 
                    DESCRICAO_ARQUIVO = COALESCE(?, DESCRICAO_ARQUIVO),
                    URL_BUCKET = COALESCE(?, URL_BUCKET)
                WHERE 
                    ID_ARQUIVO = ?
            """
            cursor.execute(query, (descricao_arquivo, url_bucket, file_id))
            conn.commit()

    def delete_file_from_id(self, file_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM CLIENTES_ARQUIVOS
                WHERE ID_ARQUIVO = ?
                """, (file_id,)
            )
            conn.commit()
