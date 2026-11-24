
import random

from sensores.sensor import Sensor


class SensorMovimento(Sensor):

    def ler(self):
        # True = movimento detectado
        # False = nenhum movimento detectado
        return random.choice([True, False])
