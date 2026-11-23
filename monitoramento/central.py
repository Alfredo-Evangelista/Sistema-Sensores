
import threading
from datetime import datetime

from configuracoes import INTERVALO_COLETA_SEGUNDOS
from sensores.temperatura import SensorTemperatura
from sensores.umidade import SensorUmidade
from sensores.movimento import SensorMovimento


class CentralMonitoramento:
    '''Coordena a coleta e a verificação dos sensores de uma única sala.'''

    def __init__(self):
        self.sensores = [
            SensorTemperatura(
                "SALA-T", "Temperatura", "Sala monitorada", "°C", 15, 30
            ),
            SensorUmidade(
                "SALA-U", "Umidade", "Sala monitorada", "%", 30, 70
            ),
            SensorMovimento(
                "SALA-M", "Movimento", "Sala monitorada", "%", 0, 85
            ),
        ]

    def coletar_todos(self):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Leituras dos sensores\n")

        for sensor in self.sensores:
            leitura = sensor.coletar()
            print(f"{leitura['sensor']}: {leitura['valor']} {leitura['unidade']}")

            if self._detectar_anomalia(sensor, leitura["valor"]):
                print(f"há uma anomalia no sensor {sensor.nome}")

    @staticmethod
    def _detectar_anomalia(sensor, valor):
        return valor < sensor.minimo or valor > sensor.maximo

    def iniciar(self):
        encerrar = threading.Event()

        def aguardar_encerramento():
            comando = input()

            if comando.strip().lower() == "x":
                encerrar.set()

        print("SenseTrack iniciado.\n")
        print("Digite X e pressione Enter para encerrar.")

        threading.Thread(
            target=aguardar_encerramento,
            daemon=True
        ).start()

        while not encerrar.is_set():
            self.coletar_todos()

            if encerrar.wait(INTERVALO_COLETA_SEGUNDOS):
                break

        print("\nMonitoramento encerrado.")
