from application.client_app import ClientApp

class IClientesApp:
    def __init__(self):
        self.client_app = ClientApp()
    
    def create_new_client(self, client):
        return self.client_app.create_new_client(client)
    
    def get_all_clients(self):
        return self.client_app.get_all_clients()
    
    def get_client_by_id(self, client_id):
        return self.client_app.get_client_by_id(client_id)
    
    def update_client_by_id(self, client_id, client):
        return self.client_app.update_client_by_id(client_id, client)
    
    def delete_client_by_id(self, client_id):
        return self.client_app.delete_client_by_id(client_id)

    def get_client_by_email(self, client_email):
        return self.client_app.get_client_by_email(client_email)