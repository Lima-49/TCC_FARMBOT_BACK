class ClientesDados:
    def __init__(self, id_arquivo=None, id_cliente=None, descricao_arquivo=None, url_bucket=None):
        self.id_arquivo = id_arquivo,
        self.id_cliente = id_cliente,
        self.descricao_arquivo = descricao_arquivo,
        self.url_bucket = url_bucket
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            id_arquivo = data.get('id_arquivo'),
            id_cliente = data.get('id_cliente'),
            descricao_arquivo = data.get('descricao_arquivo'),
            url_bucket = data.get('url_bucket')
        )
        