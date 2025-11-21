import sqlite3
from dataclasses import dataclass

@dataclass
class Atleta:
    nome: str
    cpf: str

@dataclass
class Evento:
    nome: str
    kits: dict

class InscricaoDAO:
    def __init__(self, nome_banco="inscricoes.db"):
        self.conn = sqlite3.connect(nome_banco)
        self.criar_tabelas()

    def criar_tabelas(self):
        sql = """
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atleta_nome TEXT NOT NULL,
            atleta_cpf TEXT NOT NULL,
            evento_nome TEXT NOT NULL,
            kit TEXT NOT NULL,
            termos INTEGER NOT NULL,
            aptidao INTEGER NOT NULL
        );
        """
        self.conn.execute(sql)
        self.conn.commit()

    def registrar_inscricao(self, atleta, evento, kit, termos, aptidao):
        sql = """
        INSERT INTO inscricoes (atleta_nome, atleta_cpf, evento_nome, kit, termos, aptidao)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        self.conn.execute(sql, (atleta.nome, atleta.cpf, evento.nome, kit, termos, aptidao))
        self.conn.commit()

    def atleta_ja_inscrito(self, atleta_cpf: str, evento_nome: str) -> bool:
        sql = "SELECT COUNT(*) FROM inscricoes WHERE atleta_cpf = ? AND evento_nome = ?;"
        cur = self.conn.cursor()
        cur.execute(sql, (atleta_cpf, evento_nome))
        count = cur.fetchone()[0]
        return count > 0
