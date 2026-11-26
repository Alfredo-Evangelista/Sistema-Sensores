import tkinter
from .componentes import (
    criar_titulo,
    criar_card,
    COR_FUNDO,
    COR_CARD,
    COR_TEXTO,
    COR_SECUNDARIA,
    COR_VERDE,
    COR_VERMELHO
)


class Dashboard(tkinter.Frame):
    def __init__(self, pai, central):
        super().__init__(pai, bg=COR_FUNDO)
        self.central = central
        titulo = criar_titulo(
            self,
            "Dashboard",
            "Visão geral do monitoramento"
        )
        titulo.pack(fill="x", pady=(0, 25))

        indicadores = tkinter.Frame(self, bg=COR_FUNDO)
        indicadores.pack(fill="x")

        indicadores.columnconfigure((0, 1), weight=1)

        self.card_temperatura = criar_card(indicadores, "Temperatura", "--", "Aguardando leitura")
        self.card_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.card_umidade = criar_card(indicadores, "Umidade", "--", "Aguardando leitura")
        self.card_umidade.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.card_movimento = criar_card(indicadores, "Movimento", "--", "Aguardando leitura")
        self.card_movimento.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.card_sensores = criar_card(indicadores, "Sensores ativos", "--", "Sensores cadastrados")
        self.card_sensores.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        localizacao = tkinter.Frame(self,
            bg=COR_CARD, padx=18, pady=15
        )
        localizacao.pack(fill="x", pady=20)

        tkinter.Label(
            localizacao,
            text="Localização monitorada",
            font=("Arial", 13, "bold"),
            bg=COR_CARD,
            fg=COR_TEXTO
        ).pack(anchor="w")
        tkinter.Label(
            localizacao,
            text="Sala monitorada",
            font=("Arial", 11),
            bg=COR_CARD,
            fg=COR_SECUNDARIA
        ).pack(anchor="w", pady=8)

        status = tkinter.Frame(
            self, bg=COR_CARD, padx=18, pady=15
        )
        status.pack(fill="x")
        tkinter.Label(
            status,
            text="Status do sistema",
            font=("Arial", 13, "bold"),
            bg=COR_CARD,
            fg=COR_TEXTO
        ).pack(anchor="w")
        self.label_status = tkinter.Label(
            status,
            text="Aguardando primeira coleta",
            font=("Arial", 11, "bold"),
            bg=COR_CARD,
            fg=COR_SECUNDARIA
        )
        self.label_status.pack(anchor="w", pady=8)

    def atualizar(self):
        sensores = self.central.obter_dados_sensores()
        leituras = {
            sensor["tipo"]: sensor["ultima_leitura"]
            for sensor in sensores
        }
        self.atualizar_card(self.card_temperatura,
            leituras.get("temperatura"),
            "°C"
        )
        self.atualizar_card(self.card_umidade,
            leituras.get("umidade"),
            "%"
        )
        self.atualizar_card(self.card_movimento,
            leituras.get("movimento"),
            ""
        )

        ativos = sum(1 for sensor in sensores if sensor["ativo"] )

        self.atualizar_card(self.card_sensores,
            None,
            "",
            valor=f"{ativos} / {len(sensores)}",
            descricao="Sensores ativos"
        )

        if self.central.ultima_coleta:
            self.label_status.config(
                text="● Sistema em funcionamento",
                fg=COR_VERDE
            )
    
    @staticmethod
    def atualizar_card(
        card,
        leitura,
        unidade,
        valor=None,
        descricao=None
    ):
        labels = card.winfo_children()
        if leitura is not None:
            dado = leitura["valor"]
            timestamp = leitura["timestamp"]

            if hasattr(timestamp, "strftime"):
                horario = timestamp.strftime("%H:%M:%S")
            else:
                horario = str(timestamp)[11:19]

            if isinstance(dado, bool):
                valor = "Detectado" if dado else "Sem movimento"

            else:
                valor = f"{dado:.2f} {unidade}".replace(".", ",")

            descricao = f"Última leitura: {horario}"

        if valor is not None:
            labels[1].config(text=valor)
        if descricao is not None:
            labels[2].config(text=descricao)
