import pyodbc
from models.client_model import Cliente

class ClienteRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        return pyodbc.connect(self.connection_string)

    def create_new_client(self, cliente):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO CLIENTES (NOME, SOBRE_NOME, DATA_NASCIMENTO, CPF, EMAIL, SENHA_LOGIN)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cliente.nome, cliente.sobrenome, cliente.data_nascimento, cliente.cpf, cliente.email, cliente.senha_login))
            conn.commit()

    def get_all_clients(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    ID_CLIENTE AS id_cliente, 
                    NOME AS nome, 
                    SOBRE_NOME AS sobrenome, 
                    DATA_NASCIMENTO AS data_nascimento, 
                    CPF AS cpf, 
                    EMAIL AS email, 
                    SENHA_LOGIN AS senha_login 
                FROM 
                    CLIENTES
                """
            )
            clientes = []
            for row in cursor.fetchall():
                cliente_data = {
                    'id_cliente': row[0],
                    'nome': row[1],
                    'sobrenome': row[2],
                    'data_nascimento': row[3].strftime("%d-%m-%Y"),
                    'cpf': row[4],
                    'email': row[5],
                    'senha_login': row[6]
                }
                #cliente = Cliente.from_dict(cliente_data)
                clientes.append(cliente_data)
            return clientes

    def get_client_by_id(self, id_cliente):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                    SELECT 
                        ID_CLIENTE AS id_cliente, 
                        NOME AS nome, 
                        SOBRE_NOME AS sobrenome, 
                        DATA_NASCIMENTO AS data_nascimento, 
                        CPF AS cpf, 
                        EMAIL AS email, 
                        SENHA_LOGIN AS senha_login 
                    FROM 
                        CLIENTES
                    WHERE id_cliente = ?
                """, (id_cliente,)
            )
            
            row = cursor.fetchone()
            if row:
                cliente_data = {
                    'id_cliente': row[0],
                    'nome': row[1],
                    'sobrenome': row[2],
                    'data_nascimento': row[3].strftime("%d-%m-%Y"),
                    'cpf': row[4],
                    'email': row[5],
                    'senha_login': row[6]
                }
                return Cliente.from_dict(cliente_data)
            return None

    def update_client_by_id(self, id_cliente, cliente):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE CLIENTES
                SET NOME = ?, SOBRE_NOME = ?, DATA_NASCIMENTO = ?, CPF = ?, EMAIL = ?, SENHA_LOGIN = ?
                WHERE id_cliente = ?
            """, (cliente.nome, cliente.sobrenome, cliente.data_nascimento, cliente.cpf, cliente.email, cliente.senha_login, id_cliente))
            conn.commit()

    def delete_client_by_id(self, id_cliente):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CLIENTES WHERE id_cliente = ?", (id_cliente,))
            conn.commit()

    def get_client_by_email(self, client_email):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                    SELECT                         
                        ID_CLIENTE AS id_cliente, 
                        NOME AS nome, 
                        SOBRE_NOME AS sobrenome, 
                        DATA_NASCIMENTO AS data_nascimento, 
                        CPF AS cpf, 
                        EMAIL AS email, 
                        SENHA_LOGIN AS senha_login  
                    FROM CLIENTES WHERE EMAIL = ?
                """, (client_email,)
            )
            row = cursor.fetchone()
            if row:
                cliente_data = {
                    'id_cliente': row[0],
                    'nome': row[1],
                    'sobrenome': row[2],
                    'data_nascimento': row[3].strftime("%d-%m-%Y"),
                    'cpf': row[4],
                    'email': row[5],
                    'senha_login': row[6]
                }
                return Cliente.from_dict(cliente_data)
            return None
