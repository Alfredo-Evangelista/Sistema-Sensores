# SenseTrack

Projeto em Python para simulação e monitoramento de sensores em uma única sala.

## Sensores

- Temperatura
- Umidade
- Movimento

Cada sensor possui 5% de chance de gerar uma leitura anormal em cada coleta.
Os valores são exibidos no terminal, junto de uma mensagem quando uma anomalia é detectada.

## Execução

Requisitos: Python 3.10 ou superior.

1. Abra a pasta `SenseTrack` no VS Code.
2. Abra o terminal integrado nessa pasta.
3. Execute:

   ```bash
   python main.py
   ```

O programa realiza uma coleta imediatamente ao iniciar e repete o processo a cada 8 segundos.
Para encerrar, pressione `X` no terminal.

O projeto utiliza apenas recursos da biblioteca padrão do Python; não é necessário instalar dependências externas.
