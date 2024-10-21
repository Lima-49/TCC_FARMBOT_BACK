import unittest
from unittest.mock import patch, MagicMock
from app import app

class ClientRouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('routes.client_route.IClientesApp.create_new_client')
    def test_create_new_client(self, mock_create_client):
        # Mock do resultado esperado
        mock_create_client.return_value = {'message': 'Cliente criado com sucesso'}, 201
        
        data = {
            'nome': 'Vitor',
            'sobrenome': 'Silva',
            'data_nascimento': '1990-01-01',
            'cpf': '12345678901',
            'email': 'vitor@example.com',
            'senha_login': 'senha123'
        }

        response = self.app.post('/clientes', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Cliente criado com sucesso', response.data)

    @patch('routes.client_route.IClientesApp.get_all_clients')
    def test_get_all_clients(self, mock_get_clients):
        # Mock do resultado esperado
        mock_get_clients.return_value = {'clientes': []}, 200
        
        response = self.app.get('/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'clientes', response.data)

    @patch('routes.client_route.IClientesApp.get_client_by_id')
    def test_get_cliente_by_id(self, mock_get_client):
        mock_get_client.return_value = {'nome': 'Vitor'}, 200
        
        response = self.app.get('/clientes/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vitor', response.data)

    @patch('routes.client_route.IClientesApp.update_client_by_id')
    def test_update_cliente_by_id(self, mock_update_client):
        mock_update_client.return_value = {'message': 'Cliente atualizado com sucesso'}, 200
        
        data = {
            'nome': 'Vitor',
            'sobrenome': 'Silva',
            'data_nascimento': '1990-01-01',
            'cpf': '12345678901',
            'email': 'vitor@example.com',
            'senha_login': 'senha456'
        }

        response = self.app.put('/clientes/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente atualizado com sucesso', response.data)

    @patch('routes.client_route.IClientesApp.delete_client_by_id')
    def test_delete_cliente_by_id(self, mock_delete_client):
        mock_delete_client.return_value = {'message': 'Cliente deletado com sucesso'}, 200
        
        response = self.app.delete('/clientes/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente deletado com sucesso', response.data)

    @patch('routes.client_route.IClientesApp.autentificar_login')
    def test_autentificar_login(self, mock_autentificar_login):
        mock_autentificar_login.return_value = {'message': 'Login bem-sucedido'}, 200
        
        data = {
            'email': 'vitor@example.com',
            'senha': 'senha123'
        }

        response = self.app.post('/clientes/auth', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login bem-sucedido', response.data)

if __name__ == '__main__':
    unittest.main()
