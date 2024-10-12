class ClientesDados:
    def __init__(self, id_cliente=None, descricao_arquivo=None, url_bucket=None, nome_arquivo=None, id_arquivo=None):
        self.id_arquivo = id_arquivo
        self.id_cliente = id_cliente
        self.descricao_arquivo = descricao_arquivo
        self.url_bucket = url_bucket
        self.nome_arquivo = nome_arquivo
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            id_arquivo = data.get('id_arquivo'),
            id_cliente = data.get('id_cliente'),
            descricao_arquivo = data.get('descricao_arquivo'),
            url_bucket = data.get('url_bucket'),
            nome_arquivo = data.get('nome_arquivo')
        )
        