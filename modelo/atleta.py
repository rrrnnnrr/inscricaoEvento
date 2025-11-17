class Atleta:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome.strip()
        self.cpf = cpf.strip()

    def __repr__(self):
        return f"Atleta(nome={self.nome!r}, cpf={self.cpf!r})"
