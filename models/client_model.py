class Cliente:
    def __init__(self, nome=None, sobrenome=None, data_nascimento=None, cpf=None, email=None, senha_login=None, id_cliente=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.email = email
        self.senha_login = senha_login

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_cliente=data.get('id_cliente'),
            nome=data.get('nome'),
            sobrenome=data.get('sobrenome'),
            data_nascimento=data.get('data_nascimento'),
            cpf=data.get('cpf'),
            email=data.get('email'),
            senha_login=data.get('senha_login')
        )
