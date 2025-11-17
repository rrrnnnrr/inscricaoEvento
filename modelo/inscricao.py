from dataclasses import dataclass

@dataclass
class Inscricao:
    atleta_nome: str
    atleta_cpf: str
    evento_nome: str
    kit: str
    termos_aceitos: bool
    aptidao_fisica: bool
