import tkinter


COR_FUNDO = "#F1F5F9"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#1E293B"
COR_SECUNDARIA = "#64748B"
COR_VERDE = "#16A34A"
COR_VERMELHO = "#DC2626"
COR_AZUL = "#2563EB"


def criar_titulo(pai, titulo, descricao=""):
    frame = tkinter.Frame(pai, bg=COR_FUNDO)
    tkinter.Label(
        frame,
        text=titulo,
        font=("Arial", 22, "bold"),
        fg=COR_TEXTO,
        bg=COR_FUNDO
    ).pack(anchor="w")

    if descricao:
        tkinter.Label(
            frame,
            text=descricao,
            font=("Arial", 10),
            fg=COR_SECUNDARIA,
            bg=COR_FUNDO
        ).pack(anchor="w", pady=(5, 0))
    return frame

def criar_card(pai, titulo, valor, descricao="", cor=COR_AZUL):
    card = tkinter.Frame(
        pai,
        bg=COR_CARD,
        padx=18,
        pady=15,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    tkinter.Label(
        card,
        text=titulo,
        font=("Arial", 10),
        fg=COR_SECUNDARIA,
        bg=COR_CARD
    ).pack(anchor="w")
    tkinter.Label(
        card,
        text=valor,
        font=("Arial", 24, "bold"),
        fg=cor,
        bg=COR_CARD
    ).pack(anchor="w", pady=8)

    if descricao:
        tkinter.Label(
            card,
            text=descricao,
            font=("Arial", 9),
            fg=COR_SECUNDARIA,
            bg=COR_CARD
        ).pack(anchor="w")
    return card