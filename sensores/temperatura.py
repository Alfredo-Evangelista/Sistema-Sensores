
import random

from sensores.sensor import Sensor


class SensorTemperatura(Sensor):

    CHANCE_ANOMALIA = 0.05

    def ler(self):

        if random.random() < self.CHANCE_ANOMALIA:
            return random.choice([
                random.uniform(5, 14),
                random.uniform(31, 40)
            ])

        return random.uniform(19, 27)
