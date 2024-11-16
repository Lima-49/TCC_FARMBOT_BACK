class ConfiguracaoTarefaModel:
    def __init__(self, id_cliente=None,
                 tipo_tarefa=None, produto_descr=None, fornecedor_descr=None,
                 qtd_minima=None, oferta_descr=None, fl_ativo=None,
                 fl_execucao=None, id_config_tarefa=None):
        self.id_config_tarefa = id_config_tarefa
        self.id_cliente = id_cliente
        self.tipo_tarefa = tipo_tarefa
        self.produto_descr = produto_descr  # Aqui estava correto
        self.fornecedor_descr = fornecedor_descr
        self.qtd_minima = qtd_minima
        self.oferta_descr = oferta_descr
        self.fl_ativo = fl_ativo
        self.fl_execucao = fl_execucao
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id_config_tarefa=data.get('id_config_tarefa'),
            id_cliente = data.get('id_cliente'),
            tipo_tarefa = data.get('tipo_tarefa'),
            produto_descr = data.get('produto_descr'),
            fornecedor_descr = data.get('fornecedor_descr'),
            qtd_minima = data.get('qtd_minima'),
            oferta_descr = data.get('oferta_descr'),
            fl_ativo = data.get('fl_ativo'),
            fl_execucao = data.get('fl_execucao')
        )
    