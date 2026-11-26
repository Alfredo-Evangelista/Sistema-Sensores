import json
from datetime import datetime
from pathlib import Path
from sensores.temperatura import SensorTemperatura
from sensores.umidade import SensorUmidade
from sensores.movimento import SensorMovimento


class CentralMonitoramento:
    def __init__(self):
        self.arquivo_configuracoes = (
            Path(__file__).resolve().parent.parent
            / "configuracoes.json"
        )
        self.configuracoes = self._carregar_configuracoes()
        self.sensores = [
            SensorTemperatura(
                "SALA-T",
                "Temperatura",
                "Sala monitorada",
                "°C",
                self.configuracoes["temperatura_minima"],
                self.configuracoes["temperatura_maxima"]
            ),
            SensorUmidade(
                "SALA-U",
                "Umidade",
                "Sala monitorada",
                "%",
                self.configuracoes["umidade_minima"],
                self.configuracoes["umidade_maxima"]
            ),
            SensorMovimento(
                "SALA-M",
                "Movimento",
                "Sala monitorada",
                "",
                0,
                1
            )
        ]
        self.historico = []
        self.alertas = []
        self.ultima_coleta = None

    def _carregar_configuracoes(self):
        padrao = {
            "intervalo_coleta": 8,
            "temperatura_minima": 18.0,
            "temperatura_maxima": 28.0,
            "umidade_minima": 40.0,
            "umidade_maxima": 70.0,
            "horario_movimento_inicio": "07:00",
            "horario_movimento_fim": "22:00"
        }

        if not self.arquivo_configuracoes.exists():
            self._salvar_arquivo_configuracoes(padrao)
            return padrao

        try:
            with open(
                self.arquivo_configuracoes,
                "r",
                encoding="utf-8"
            ) as arquivo:
                dados = json.load(arquivo)

            padrao.update(dados)
        except (json.JSONDecodeError, OSError, TypeError):
            print("Não foi possível carregar as configurações. Usando valores padrão.")
            self._salvar_arquivo_configuracoes(padrao)
        return padrao

    def _salvar_arquivo_configuracoes(self, configuracoes):
        with open(self.arquivo_configuracoes,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                configuracoes,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    @property
    def intervalo_coleta_segundos(self):
        return self.configuracoes["intervalo_coleta"]

    def atualizar_configuracoes(self,
        temperatura_minima,
        temperatura_maxima,
        umidade_minima,
        umidade_maxima,
        horario_inicio,
        horario_fim,
        intervalo_coleta
    ):
        novas_configuracoes = {
            "intervalo_coleta": intervalo_coleta,
            "temperatura_minima": temperatura_minima,
            "temperatura_maxima": temperatura_maxima,
            "umidade_minima": umidade_minima,
            "umidade_maxima": umidade_maxima,
            "horario_movimento_inicio": horario_inicio,
            "horario_movimento_fim": horario_fim
        }
        self.sensores[0].minimo = temperatura_minima
        self.sensores[0].maximo = temperatura_maxima
        self.sensores[1].minimo = umidade_minima
        self.sensores[1].maximo = umidade_maxima
        self.configuracoes.update(novas_configuracoes)
        self._salvar_arquivo_configuracoes(self.configuracoes)

    def _movimento_fora_do_horario(self, timestamp):
        horario_inicio = datetime.strptime(
            self.configuracoes["horario_movimento_inicio"],
            "%H:%M"
        ).time()
        horario_fim = datetime.strptime(
            self.configuracoes["horario_movimento_fim"],
            "%H:%M"
        ).time()

        horario_atual = timestamp.time()

        if horario_inicio == horario_fim:
            return False

        if horario_inicio < horario_fim:
            return not (
                horario_inicio <= horario_atual < horario_fim
            )

        return not (
            horario_atual >= horario_inicio
            or horario_atual < horario_fim
        )

    def _detectar_anomalia(self, sensor, valor, timestamp):
        if sensor.tipo == "movimento":
            return (
                valor is True
                and self._movimento_fora_do_horario(timestamp)
            )
        return valor < sensor.minimo or valor > sensor.maximo

    def _registrar_leitura(self, sensor, valor, timestamp):
        leitura = {
            "sensor_id": sensor.id,
            "sensor": sensor.nome,
            "local": sensor.local,
            "tipo": sensor.tipo,
            "valor": valor,
            "unidade": sensor.unidade,
            "timestamp": timestamp
        }
        anomalia = self._detectar_anomalia(
            sensor,
            valor,
            timestamp
        )
        leitura["anomalia"] = anomalia
        sensor.ultima_leitura = leitura
        self.historico.append(leitura)

        if anomalia:
            alerta = {
                "sensor": sensor.nome,
                "local": sensor.local,
                "valor": valor,
                "timestamp": timestamp,
                "mensagem": (
                    f"Anomalia detectada no sensor {sensor.nome}"
                )
            }
            self.alertas.append(alerta)

        print(
            f"{sensor.nome}: {valor} "
            f"{sensor.unidade} "
            f"{' - ANOMALIA' if anomalia else ''}"
        )
        return leitura

    def receber_leituras(self, dados):
        timestamp = datetime.now()
        leituras = []

        valores = [
            dados["temperatura"],
            dados["umidade"],
            dados["movimento"]
        ]

        for sensor, valor in zip(self.sensores, valores):
            if sensor.tipo == "movimento":
                if not isinstance(valor, bool):
                    raise ValueError("Valor de movimento inválido.")
            else:
                if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                    raise ValueError(f"Valor inválido para {sensor.nome}.")
                valor = float(valor)

            leitura = self._registrar_leitura(
                sensor,
                valor,
                timestamp
            )
            leituras.append(leitura)

        self.ultima_coleta = timestamp
        return leituras

    def coletar_todos(self):
        leituras = []
        self.ultima_coleta = datetime.now()

        for sensor in self.sensores:
            leitura = sensor.coletar()
            timestamp = self.ultima_coleta
            leitura["timestamp"] = timestamp
            anomalia = self._detectar_anomalia(
                sensor,
                leitura["valor"],
                timestamp
            )

            leitura["anomalia"] = anomalia
            self.historico.append(leitura)
            leituras.append(leitura)

            if anomalia:
                alerta = {
                    "sensor": sensor.nome,
                    "local": sensor.local,
                    "valor": leitura["valor"],
                    "timestamp": timestamp,
                    "mensagem": (
                        f"Anomalia detectada no sensor {sensor.nome}"
                    )
                }
                self.alertas.append(alerta)

            print(
                f"{sensor.nome}: {leitura['valor']} "
                f"{sensor.unidade} "
                f"{' - ANOMALIA' if anomalia else ''}"
            )
        return leituras

    def obter_dados_sensores(self):
        return [
            sensor.dados_publicos()
            for sensor in self.sensores
        ]

    def obter_historico(self):
        return self.historico

    def obter_alertas(self):
        return self.alertas
