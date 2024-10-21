from unittest import TestCase
from unittest.mock import patch, MagicMock
from repository.client_repository import ClienteRepository
from models.client_model import Cliente
from datetime import datetime

class TestClienteRepository(TestCase):
    def setUp(self):
        self.connection_string = "Driver={SQL Server};Server=server;Database=db;UID=user;PWD=pass;"
        self.repo = ClienteRepository(self.connection_string)

    @patch('pyodbc.connect')
    def test_create_new_client(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Cliente simulado
        cliente = Cliente("John", "Doe", "01-01-1990", "12345678901", "john@example.com", "password")

        # Executar o método de criação de cliente
        self.repo.create_new_client(cliente)

        # Verificar se o método 'execute' foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            """ 
                INSERT INTO CLIENTES (NOME, SOBRE_NOME, DATA_NASCIMENTO, CPF, EMAIL, SENHA_LOGIN)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cliente.nome, cliente.sobrenome, cliente.data_nascimento, cliente.cpf, cliente.email, cliente.senha_login)
        )
        # Verificar se o commit foi chamado
        mock_conn.commit.assert_called_once()

    @patch('pyodbc.connect')
    def test_delete_client_by_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Executar o método de deletar cliente
        self.repo.delete_client_by_id(1)

        # Verificar se o método 'execute' foi chamado corretamente
        mock_cursor.execute.assert_called_once_with("DELETE FROM CLIENTES WHERE id_cliente = ?", (1,))
        # Verificar se o commit foi chamado
        mock_conn.commit.assert_called_once()

    @patch('pyodbc.connect')
    def test_get_all_clients(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular os dados retornados pelo fetchall()
        mock_cursor.fetchall.return_value = [
            (1, 'John', 'Doe', datetime.strptime("01-01-1990", "%d-%m-%Y"), '12345678901', 'john@example.com', 'password')
        ]

        # Executar o método para obter todos os clientes
        result = self.repo.get_all_clients()

        # Verificar o tamanho da lista retornada
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['nome'], 'John')

    @patch('pyodbc.connect')
    def test_get_client_by_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular os dados retornados pelo fetchone()
        mock_cursor.fetchone.return_value = (1, 'John', 'Doe', datetime.strptime("01-01-1990", "%d-%m-%Y"), '12345678901', 'john@example.com', 'password')

        # Executar o método para obter cliente por ID
        result = self.repo.get_client_by_id(1)

        # Verificar os dados retornados
        self.assertEqual(result.nome, 'John')

    @patch('pyodbc.connect')
    def test_update_client_by_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Cliente simulado
        cliente = Cliente("John", "Doe", "01-01-1990", "12345678901", "john@example.com", "newpassword")

        # Executar o método de atualizar cliente
        self.repo.update_client_by_id(1, cliente)

        # Verificar se o método 'execute' foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            """
                UPDATE CLIENTES
                SET NOME = ?, SOBRE_NOME = ?, DATA_NASCIMENTO = ?, CPF = ?, EMAIL = ?, SENHA_LOGIN = ?
                WHERE id_cliente = ?
            """, (cliente.nome, cliente.sobrenome, cliente.data_nascimento, cliente.cpf, cliente.email, cliente.senha_login, 1)
        )
        # Verificar se o commit foi chamado
        mock_conn.commit.assert_called_once()
