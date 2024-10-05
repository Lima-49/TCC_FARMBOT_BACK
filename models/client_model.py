import bcrypt

class Cliente:
    def __init__(self, nome=None, sobrenome=None, data_nascimento=None, cpf=None, email=None, senha_login=None, client_id=None):
        self.client_id = client_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.email = email
        self.senha_login = senha_login

    @classmethod
    def from_dict(cls, data):
        return cls(
            client_id=data.get('client_id'),
            nome=data.get('nome'),
            sobrenome=data.get('sobrenome'),
            data_nascimento=data.get('data_nascimento'),
            cpf=data.get('cpf'),
            email=data.get('email'),
            senha_login=data.get('senha_login')
        )

    def hash_senha(self, senha):
        # Gera um salt aleatório
        salt = bcrypt.gensalt()
        # Gera o hash da senha
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return senha_hashed
