import tkinter
from .componentes import (
    criar_titulo,
    COR_FUNDO,
    COR_CARD,
    COR_TEXTO,
    COR_SECUNDARIA,
    COR_VERDE
)


class LocalizacoesView(tkinter.Frame):
    def __init__(self, pai, central):
        super().__init__(pai, bg=COR_FUNDO)
        self.central = central
        super().__init__(pai, bg=COR_FUNDO)

        titulo = criar_titulo(
            self,
            "Localizações",
            "Ambientes cadastrados no sistema"
        )
        titulo.pack(fill="x", pady=(0, 25))
        ambientes = [
            ("Sala 01", "2 sensores", "Monitorando"),
        ]

        for nome, quantidade, estado in ambientes:
            card = tkinter.Frame(
                self,
                bg=COR_CARD,
                padx=20,
                pady=20
            )
            card.pack(fill="x", pady=6)
            tkinter.Label(
                card,
                text=nome,
                font=("Arial", 14, "bold"),
                bg=COR_CARD,
                fg=COR_TEXTO
            ).pack(anchor="w")
            tkinter.Label(
                card,
                text=quantidade,
                font=("Arial", 10),
                bg=COR_CARD,
                fg=COR_SECUNDARIA
            ).pack(anchor="w", pady=5)
            tkinter.Label(
                card,
                text=f"● {estado}",
                font=("Arial", 10),
                bg=COR_CARD,
                fg=COR_VERDE
            ).pack(anchor="w")
