import random

from configuracoes import CHANCE_ANOMALIA
from .sensor import Sensor


class SensorUmidade(Sensor):
    def ler(self):
        if random.random() < CHANCE_ANOMALIA:
            return random.choice([random.uniform(10, 29), random.uniform(71, 95)])
        return random.uniform(40, 65)
