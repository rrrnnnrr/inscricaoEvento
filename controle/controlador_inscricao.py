from modelo.banco_dados import BancoDeDados

class ControladorInscricao:
    def __init__(self):
        self.banco = BancoDeDados()

    def validar_dados(self, atleta, termos_aceitos, aptidao_fisica, evento_nome):
        erros = []

        if not atleta.nome:
            erros.append("Nome não pode estar vazio.")
        if not atleta.cpf:
            erros.append("CPF não pode estar vazio.")
        else:
            only_digits = ''.join(filter(str.isdigit, atleta.cpf))
            if len(only_digits) != 11:
                erros.append("CPF deve conter 11 dígitos (somente números).")

        if self.banco.atleta_ja_inscrito(atleta.cpf, evento_nome):
            erros.append("Você já está inscrito neste evento.")

        if not termos_aceitos and not aptidao_fisica:
            erros.append("Você deve aceitar os termos de responsabilidade e atestar aptidão física.")
        else:
            if not termos_aceitos:
                erros.append("Você deve aceitar os termos de responsabilidade.")
            if not aptidao_fisica:
                erros.append("Você deve atestar aptidão física.")

        return (len(erros) == 0, erros)

    def registrar_inscricao(self, atleta, evento, kit, termos, aptidao):
        self.banco.registrar_inscricao(atleta, evento, kit, termos, aptidao)
