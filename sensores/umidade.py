
import random

from sensores.sensor import Sensor


class SensorUmidade(Sensor):

    CHANCE_ANOMALIA = 0.05

    def ler(self):

        if random.random() < self.CHANCE_ANOMALIA:
            return random.choice([
                random.uniform(10, 29),
                random.uniform(71, 95)
            ])

        return random.uniform(40, 65)
