import bcrypt

class Login:
    def __init__(self, email=None, senha=None):
        self.email = email
        self.senha = senha

    def hash_senha(self, senha):
        # Gera um salt aleatório
        salt = bcrypt.gensalt()
        # Gera o hash da senha
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return senha_hashed

    def verificar_senha(self, senha_fornecida, senha_hashed):
        # Verifica se a senha fornecida corresponde ao hash
        return bcrypt.checkpw(senha_fornecida.encode('utf-8'), senha_hashed.encode('utf-8'))
    