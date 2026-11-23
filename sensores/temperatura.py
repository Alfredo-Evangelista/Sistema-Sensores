import random

from configuracoes import CHANCE_ANOMALIA
from .sensor import Sensor


class SensorTemperatura(Sensor):
    def ler(self):
        if random.random() < CHANCE_ANOMALIA:
            return random.choice([random.uniform(5, 14), random.uniform(31, 40)])
        return random.uniform(19, 27)



