from monitoramento.central import CentralMonitoramento
from interface.janela_principal import JanelaPrincipal
from servidor import ServidorSensores


if __name__ == "__main__":
    central = CentralMonitoramento()

    servidor = ServidorSensores(central)
    servidor.iniciar()

    janela = JanelaPrincipal(central, servidor)
    janela.iniciar()
