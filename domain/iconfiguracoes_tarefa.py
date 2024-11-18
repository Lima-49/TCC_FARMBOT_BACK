from application.configuracoes_tarefa_app import ConfiguracoesTarefaApp

class IConfiguracoesTarefasApp:
    def __init__(self):
        self.configuracoes_tarefas = ConfiguracoesTarefaApp()
    
    def add_new_config_job(self, config_tarefa):
        return self.configuracoes_tarefas.add_new_file(config_tarefa)
    
    def get_config_jobs(self, client_id):
        return self.configuracoes_tarefas.get_config_jobs(client_id)
    
    def obtendo_lista(self, id_cliente, tipo_arquivo, coluna_lista):
        return self.configuracoes_tarefas.obtendo_lista(id_cliente, tipo_arquivo, coluna_lista)