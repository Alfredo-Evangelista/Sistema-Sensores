import random
from sensores.sensor import Sensor


class SensorMovimento(Sensor):
    def ler(self):
        return random.choice([True, False])
