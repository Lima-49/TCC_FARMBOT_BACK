from unittest import TestCase
from unittest.mock import patch, MagicMock
from repository.client_arquivos_repository import ClientDadosRepository
from models.client_arquivos_model import ClientesDados

class TestClientDadosRepository(TestCase):
    def setUp(self):
        self.connection_string = "Driver={SQL Server};Server=server;Database=db;UID=user;PWD=pass;"
        self.repo = ClientDadosRepository(self.connection_string)

    @patch('pyodbc.connect')
    def test_add_new_file(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulated client data
        client_data = ClientesDados(id_cliente=1, descricao_arquivo='Arquivo Teste',
                                    url_bucket='http://example.com/arquivo', nome_arquivo='arquivo.txt')

        # Execute the method
        self.repo.add_new_file(client_data)

        # Expected SQL statement
        expected_query = """
            INSERT INTO CLIENTES_ARQUIVOS (ID_CLIENTE, DESCRICAO_ARQUIVO, URL_BUCKET, NOME_ARQUIVO)
            VALUES (?, ?, ?, ?)
        """.strip()

        # Verify if the expected query was executed
        actual_query = mock_cursor.execute.call_args[0][0].strip()
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(mock_cursor.execute.call_args[0][1], (client_data.id_cliente, client_data.descricao_arquivo, client_data.url_bucket, client_data.nome_arquivo))

        mock_conn.commit.assert_called_once()


    @patch('pyodbc.connect')
    def test_get_client_files(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular os dados retornados pelo fetchall()
        mock_cursor.fetchall.return_value = [
            (1, 1, 'Arquivo Teste', 'http://example.com/arquivo', 'arquivo.txt')
        ]

        # Executar o método para obter arquivos do cliente
        result = self.repo.get_client_files(1)

        # Verificar o tamanho da lista retornada
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['descricao_arquivo'], 'Arquivo Teste')

    @patch('pyodbc.connect')
    def test_get_file_from_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular os dados retornados pelo fetchone()
        mock_cursor.fetchone.return_value = (1, 1, 'Arquivo Teste', 'http://example.com/arquivo', 'arquivo.txt')

        # Executar o método para obter arquivo por ID
        result = self.repo.get_file_from_id(1)

        # Verificar os dados retornados
        self.assertEqual(result.id_arquivo, 1)
        self.assertEqual(result.descricao_arquivo, 'Arquivo Teste')

    @patch('pyodbc.connect')
    def test_update_file_from_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Executar o método para atualizar arquivo
        self.repo.update_file_from_id(1, descricao_arquivo='Arquivo Atualizado')

        # Verificar se o método 'execute' foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            """
                UPDATE CLIENTES_ARQUIVOS
                SET 
                    DESCRICAO_ARQUIVO = COALESCE(?, DESCRICAO_ARQUIVO),
                    URL_BUCKET = COALESCE(?, URL_BUCKET)
                WHERE 
                    ID_ARQUIVO = ?
            """, ('Arquivo Atualizado', None, 1)
        )
        # Verificar se o commit foi chamado
        mock_conn.commit.assert_called_once()

    @patch('pyodbc.connect')
    def test_delete_file_from_id(self, mock_connect):
        # Mock da conexão e do cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Executar o método para deletar arquivo
        self.repo.delete_file_from_id(1)

        # Verificar se o método 'execute' foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            """
            DELETE FROM CLIENTES_ARQUIVOS
            WHERE ID_ARQUIVO = ?
            """.strip(),  # Removendo espaços em branco e quebras de linha
            (1,)
        )
        # Verificar se o commit foi chamado
        mock_conn.commit.assert_called_once()

