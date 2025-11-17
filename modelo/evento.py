class Evento:
    def __init__(self, nome: str, kits: dict):
        self.nome = nome
        self.kits = dict(kits)

    def obter_kits(self):
        itens = []
        for kit_nome, preco in self.kits.items():
            itens.append(f"{kit_nome} R${preco:.2f}")
        return itens

    def __repr__(self):
        return f"Evento(nome={self.nome!r}, kits={self.kits!r})"
