from flask import Blueprint, request
from models.configuracoes_tarefas_model import ConfiguracaoTarefaModel
from domain.iconfiguracoes_tarefa import IConfiguracoesTarefasApp

configTarefaModel = ConfiguracaoTarefaModel()
config_tarefa_bp = Blueprint('configuracoes_tarefas', __name__)
iconfig_tarefa = IConfiguracoesTarefasApp()

@config_tarefa_bp.route('/configuracao-tarefa', methods=['POST'])
def add_new_config_job():
    data = request.json
    config_tarefa = ConfiguracaoTarefaModel(data['id_cliente'], data['tipo_tarefa'], data['produto_descr'],
                                            data['fornecedor_descr'], data['qtd_minima'], data['oferta_descr'],
                                            data['fl_ativo'], data['fl_execucao'])
    
    result = iconfig_tarefa.add_new_config_job(config_tarefa)
    
    return result

@config_tarefa_bp.route('/configuracao-tarefa/<int:client_id>', methods=['GET'])
def get_config_jobs(client_id):
    result = iconfig_tarefa.get_config_jobs(client_id)
    return result  

@config_tarefa_bp.route("/configuracao-tarefa/lista-fornecedores/<int:client_id>/<int:tipo_arquivo>/<string:coluna_lista>", methods=['GET'])
def obtendo_lista_de_fornecedores(client_id, tipo_arquivo, coluna_lista):
    result = iconfig_tarefa.obtendo_lista_de_fornecedores(client_id, tipo_arquivo,coluna_lista)
    return result