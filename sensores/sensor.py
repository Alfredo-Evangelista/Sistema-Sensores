
from datetime import datetime
from abc import ABC, abstractmethod
from excecoes import SensorInativoError, FalhaLeituraError


class Sensor(ABC):
    """Classe abstrata que define o comportamento comum dos sensores."""

    def __init__(self, sensor_id, nome, local, unidade, minimo, maximo):
        self.id = sensor_id
        self.nome = nome
        self.local = local
        self.unidade = unidade
        self.minimo = minimo
        self.maximo = maximo
        self.ativo = True
        self.ultima_leitura = None

    @abstractmethod
    def ler(self):
        """Obtém uma leitura. Cada sensor implementa sua própria lógica."""
        raise NotImplementedError

    def coletar(self):
        valor = self.ler()

        # Sensores numéricos continuam utilizando float.
        # O sensor de movimento mantém o valor booleano.
        if not isinstance(valor, bool):
            valor = float(valor)

        leitura = {
            "sensor_id": self.id,
            "sensor": self.nome,
            "local": self.local,
            "tipo": self.tipo,
            "valor": valor,
            "unidade": self.unidade,
            "timestamp": datetime.now()
        }

        self.ultima_leitura = leitura

        return leitura

    @property
    def tipo(self):
        return self.__class__.__name__.replace("Sensor", "").lower()

    def dados_publicos(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "local": self.local,
            "unidade": self.unidade,
            "ativo": self.ativo,
            "minimo": self.minimo,
            "maximo": self.maximo,
            "ultima_leitura": self.ultima_leitura
        }
