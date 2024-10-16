from application.client_app import ClientApp

class IClientesApp:
    def __init__(self):
        self.client_app = ClientApp()
    
    def create_new_client(self, client):
        return self.client_app.create_new_client(client)
    
    def get_all_clients(self):
        return self.client_app.get_all_clients()
    
    def get_client_by_id(self, id_cliente):
        return self.client_app.get_client_by_id(id_cliente)
    
    def update_client_by_id(self, id_cliente, client):
        return self.client_app.update_client_by_id(id_cliente, client)
    
    def delete_client_by_id(self, id_cliente):
        return self.client_app.delete_client_by_id(id_cliente)

    def autentificar_login(self, login):
        return self.client_app.autentificar_login(login)