class ErroMonitoramento(Exception):
    '''Erro geral ocorrido durante o monitoramento.'''


class SensorInativoError(ErroMonitoramento):
    '''Tentativa de leitura de um sensor desativado.'''


class FalhaLeituraError(ErroMonitoramento):
    '''Falha ao obter ou validar uma leitura do sensor.'''
