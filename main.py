from monitoramento.central import CentralMonitoramento
from interface.janela_principal import JanelaPrincipal


if __name__ == "__main__":

    central = CentralMonitoramento()

    janela = JanelaPrincipal(central)
    janela.iniciar()
