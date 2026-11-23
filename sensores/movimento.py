import random

from configuracoes import CHANCE_ANOMALIA
from .sensor import Sensor


class SensorMovimento(Sensor):
    def ler(self):
        if random.random() < CHANCE_ANOMALIA:
            return random.uniform(86, 100)
        return random.uniform(0, 55)
