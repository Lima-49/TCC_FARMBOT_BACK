import unittest
from unittest.mock import patch, MagicMock
from app import app

class ClientArquivosRouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('routes.client_arquivos_route.IClientesArquivosApp.add_new_file')
    def test_add_new_file(self, mock_add_file):
        mock_add_file.return_value = {'message': 'Arquivo adicionado com sucesso'}, 201
        
        data = {
            'id_cliente': 1,
            'descricao_arquivo': 'Contrato',
            'url_bucket': 'https://storage.googleapis.com/bucket/contrato.pdf',
            'nome_arquivo': 'contrato.pdf'
        }

        response = self.app.post('/files', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Arquivo adicionado com sucesso', response.data)

    @patch('routes.client_arquivos_route.IClientesArquivosApp.get_client_files')
    def test_get_client_files(self, mock_get_files):
        mock_get_files.return_value = {'arquivos': []}, 200
        
        response = self.app.get('/files/1/files')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'arquivos', response.data)

    @patch('routes.client_arquivos_route.IClientesArquivosApp.get_file_from_id')
    def test_get_file_from_id(self, mock_get_file):
        mock_get_file.return_value = {'nome_arquivo': 'contrato.pdf'}, 200
        
        response = self.app.get('/files/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'contrato.pdf', response.data)

    @patch('routes.client_arquivos_route.IClientesArquivosApp.update_file_from_id')
    def test_update_file_from_id(self, mock_update_file):
        mock_update_file.return_value = {'message': 'Arquivo atualizado com sucesso'}, 200
        
        data = {
            'descricao_arquivo': 'Contrato atualizado',
            'url_bucket': 'https://storage.googleapis.com/bucket/contrato_atualizado.pdf'
        }

        response = self.app.put('/files/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Arquivo atualizado com sucesso', response.data)

    @patch('routes.client_arquivos_route.IClientesArquivosApp.delete_file_from_id')
    def test_delete_file_from_id(self, mock_delete_file):
        mock_delete_file.return_value = {'message': 'Arquivo deletado com sucesso'}, 200
        
        response = self.app.delete('/files/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Arquivo deletado com sucesso', response.data)

    @patch('routes.client_arquivos_route.IClientesArquivosApp.add_file_from_request')
    def test_upload_file(self, mock_upload_file):
        mock_upload_file.return_value = {'message': 'Arquivo enviado com sucesso'}, 201

        # Simulando envio de arquivo
        with open(r'tests\vendas.csv', 'rb') as file:
            data = {
                'file': file
            }

            response = self.app.post('/files/1/upload-file', data=data)
            
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Arquivo enviado com sucesso', response.data)

if __name__ == '__main__':
    unittest.main()
