from modelo.banco_dados import InscricaoDAO
from controle.controlador_inscricao import ControladorInscricao
from modelo.evento import Evento
from modelo.atleta import Atleta
from visao.tela_inscricao import TelaInscricao
from pathlib import Path

def main():
    banco = None
    try:
        project_dir = Path(__file__).resolve().parent
        db_path = project_dir / "inscricoes.db"
        banco = InscricaoDAO(str(db_path))
        controlador = ControladorInscricao()

        kits = {
            "Completo": 75.00,
            "Camiseta": 50.00,
            "Sem Kit": 0.00
        }
        evento = Evento("Maratona 123", kits)

        atleta_exemplo = Atleta("Ruan", "04403155901")

        tela = TelaInscricao(controlador, evento, atleta_exemplo)
        tela.abrir()
    finally:
        if banco is not None:
            banco.conn.close()

if __name__ == "__main__":
    main()
