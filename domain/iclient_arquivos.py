from application.client_arquivos_app import ClientesArquivos

class IClientesArquivosApp:
    def __init__(self):
        self.client_arquivos = ClientesArquivos()
        
    def add_new_file(self, client_arquivo):
        return self.client_arquivos.add_new_file(client_arquivo)
    
    def get_client_files(self, client_id):
        return self.client_arquivos.get_client_files(client_id)
    
    def get_file_from_id(self, file_id):
        return self.client_arquivos.get_file_from_id(file_id)
    
    def update_file_from_id(self, file_id, descricao_arquivo=None, url_bucket=None):
        return self.client_arquivos.update_file_from_id(file_id, descricao_arquivo, url_bucket)
    
    def delete_file_from_id(self, file_id):
        return self.client_arquivos.delete_file_from_id(file_id)
    
    def add_file_from_request(self, client_id, file):
        return self.client_arquivos.add_file_from_request(client_id, file)
    
    def return_file_as_json(self, client_id, tipo_arquivo):
        return self.client_arquivos.return_file_as_json(client_id, tipo_arquivo)