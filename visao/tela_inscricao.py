import FreeSimpleGUI as sg
# import PySimpleGUI as sg
from modelo.atleta import Atleta
from controle.controlador_inscricao import ControladorInscricao
from . import fichaMedica

class TelaInscricao:
    def __init__(self, controlador: ControladorInscricao, evento, atleta: Atleta):
        self.controlador = controlador
        self.evento = evento
        self.atleta = atleta

    def abrir(self):
        sg.theme('DarkBlue14')

        termo_responsabilidade = """
Declaro que participo deste evento por livre e espontânea vontade,
isentando de qualquer responsabilidade os organizadores, patrocinadores
e realizadores, em meu nome e de meus sucessores. Declaro estar em
boas condições de saúde e ter treinado apropriadamente para a prova.
"""

        try:
            combo_items = self.evento.obter_kits()
        except Exception:
            combo_items = [f"{k} R${v:.2f}" for k, v in self.evento.kits.items()]

        default_combo = combo_items[0] if combo_items else ''

        layout = [
            [sg.Text(f'Inscrição: {self.evento.nome}', font=('Helvetica', 20))],
            [sg.HorizontalSeparator()],
            [sg.Text('Confirme seus dados cadastrais:')],
            [sg.Text('Nome:'), sg.Text(self.atleta.nome, key='-NOME-', size=(40,1))],
            [sg.Text('CPF:'), sg.Text(self.atleta.cpf, key='-CPF-', size=(20,1))],
            [sg.HorizontalSeparator()],
            [sg.Text('Escolha do Kit*', size=(15,1)),
             sg.Combo(combo_items, default_value=default_combo, readonly=True, key='-KIT-', size=(30,1))],
            [sg.HorizontalSeparator()],
            [sg.Text('Ficha Médica e Termo de Responsabilidade', font=('Helvetica', 12))],
            [sg.Text('Preencha a ficha médica'), sg.Button('Preencher', key='-FICHA_MEDICA-', size=(10,1))],
            [sg.Multiline(default_text=termo_responsabilidade, disabled=True, size=(60, 8), autoscroll=True)],
            [sg.Checkbox('Li e aceito os termos de responsabilidade e isenção de riscos.', key='-TERMO_ACEITO-')],
            [sg.Checkbox('Atesto que estou em condições de saúde aptas para a prática da atividade física.', key='-SAUDE_OK-')],
            [sg.VPush()],
            [sg.Button('Confirmar Inscrição', key='-CONFIRMAR-'), sg.Button('Voltar', key='-VOLTAR-')]
        ]

        janela = sg.Window('PaceHub - Inscrição', layout, size=(500, 500), finalize=True, resizable=True)

        ficha_preenchida = False

        while True:
            event, values = janela.read()
            if event in (sg.WIN_CLOSED, '-VOLTAR-'):
                break

            if event == '-FICHA_MEDICA-':
                janela_ficha = fichaMedica.criar_janela_ficha_medica()
                while True:
                    event_ficha, values_ficha = janela_ficha.read()
                    if event_ficha in (sg.WIN_CLOSED, '-VOLTAR-'):
                        break
                    if event_ficha == '-SALVAR-':
                        if not values_ficha.get('-DECLARACAO_SAUDE-', False):
                            sg.popup_error('Você precisa atestar sua condição de saúde.')
                            continue

                        respostas_sim = [
                            values_ficha.get('-PERGUNTA1_SIM-', False),
                            values_ficha.get('-PERGUNTA2_SIM-', False),
                            values_ficha.get('-PERGUNTA3_SIM-', False),
                            values_ficha.get('-PERGUNTA4_SIM-', False),
                            values_ficha.get('-PERGUNTA5_SIM-', False),
                            values_ficha.get('-PERGUNTA6_SIM-', False),
                            values_ficha.get('-PERGUNTA7_SIM-', False)
                        ]

                        if any(respostas_sim):
                            sg.popup('ATENÇÃO: Uma ou mais respostas indicam que você deve consultar um médico antes de praticar atividade física.\n\nRecomendamos que você procure orientação médica antes de participar do evento.')

                        sg.popup('Ficha médica salva com sucesso!')
                        ficha_preenchida = True
                        break

                janela_ficha.close()

            if event == '-CONFIRMAR-':
                if not ficha_preenchida:
                    sg.popup_error('Você deve preencher a ficha médica antes de finalizar inscrição.')
                    continue

                nome = self.atleta.nome.strip()
                cpf = self.atleta.cpf.strip()
                atleta_atual = Atleta(nome, cpf)
                termos = bool(values.get('-TERMO_ACEITO-', False))
                aptidao = bool(values.get('-SAUDE_OK-', False))
                kit = values.get('-KIT-', '')

                ok, erros = self.controlador.validar_dados(atleta_atual, termos, aptidao, self.evento.nome)
                if ok:
                    self.controlador.registrar_inscricao(atleta_atual, self.evento, kit, termos, aptidao)
                    sg.popup(f'Inscrição realizada com sucesso!\n\nKit Selecionado: {kit}')
                    break
                else:
                    mensagem = "\n".join(erros)
                    sg.popup_error(f"Erro ao validar inscrição:\n\n{mensagem}")

        janela.close()
