import tkinter
from .componentes import (
    criar_titulo,
    COR_FUNDO,
    COR_CARD,
    COR_TEXTO,
    COR_SECUNDARIA,
    COR_VERMELHO,
    COR_VERDE
)


class AlertasView(tkinter.Frame):
    def __init__(self, pai, central):
        super().__init__(pai, bg=COR_FUNDO)
        self.central = central
        titulo = criar_titulo(self,
            "Alertas",
            "Eventos e anomalias identificados"
        )
        titulo.pack(fill="x", pady=(0, 25))
        self.lista_alertas = tkinter.Frame(self,
            bg=COR_FUNDO
        )
        self.lista_alertas.pack(fill="both", expand=True)

    def atualizar(self):
        for widget in self.lista_alertas.winfo_children():
            widget.destroy()
        alertas = self.central.obter_alertas()

        if not alertas:
            tkinter.Label(self.lista_alertas,
                text="Nenhuma anomalia detectada.",
                font=("Arial", 12),
                bg=COR_FUNDO,
                fg=COR_VERDE
            ).pack(anchor="w", pady=10)
            return

        for alerta in reversed(alertas):
            card = tkinter.Frame(self.lista_alertas,
                bg=COR_CARD,
                padx=20,
                pady=18
            )
            card.pack(fill="x", pady=6)
            tkinter.Label(
                card,
                text=alerta["mensagem"],
                font=("Arial", 12, "bold"),
                bg=COR_CARD,
                fg=COR_VERMELHO
            ).pack(anchor="w")
            tkinter.Label(
                card,
                text=(
                    f"{alerta['sensor']} | "
                    f"{alerta['horario'].replace('T', ' ')} | "
                    f"{alerta['valor']} {alerta['unidade']}"
                ),
                font=("Arial", 10),
                bg=COR_CARD,
                fg=COR_SECUNDARIA
            ).pack(anchor="w", pady=5)
