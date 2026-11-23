from abc import ABC, abstractmethod
from datetime import datetime
from excecoes import SensorInativoError, FalhaLeituraError


class Sensor(ABC):
    '''Classe abstrata que define o comportamento comum dos sensores.'''

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
        '''Obtém uma leitura. Cada sensor implementa sua própria lógica.'''
        raise NotImplementedError

    def coletar(self):
        if not self.ativo:
            raise SensorInativoError(f"O sensor {self.nome} está inativo.")

        try:
            valor = float(self.ler())
            self.ultima_leitura = {
                "sensor_id": self.id,
                "sensor": self.nome,
                "local": self.local,
                "tipo": self.tipo,
                "valor": round(valor, 2),
                "unidade": self.unidade,
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }
            return self.ultima_leitura
        except SensorInativoError:
            raise
        except Exception as erro:
            raise FalhaLeituraError(
                f"Não foi possível ler {self.nome}: {erro}"
            ) from erro

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



