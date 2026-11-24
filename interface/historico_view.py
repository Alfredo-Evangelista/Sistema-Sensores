
import tkinter
from tkinter import ttk
from datetime import datetime

from .componentes import criar_titulo, COR_FUNDO


class HistoricoView(tkinter.Frame):

    def __init__(self, pai, central):
        super().__init__(pai, bg=COR_FUNDO)

        self.central = central

        titulo = criar_titulo(
            self,
            "Histórico",
            "Registro das medições realizadas"
        )
        titulo.pack(fill="x", pady=(0, 25))

        estilo = ttk.Style()

        estilo.configure(
            "Historico.Treeview",
            font=("Arial", 10),
            rowheight=35,
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF"
        )

        estilo.configure(
            "Historico.Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#E2E8F0",
            foreground="#1E293B",
            padding=10
        )

        container = tkinter.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(
            container,
            columns=("horario", "sensor", "valor", "local"),
            show="headings",
            style="Historico.Treeview"
        )

        self.tabela.heading("horario", text="Horário")
        self.tabela.heading("sensor", text="Sensor")
        self.tabela.heading("valor", text="Medição")
        self.tabela.heading("local", text="Localização")

        self.tabela.column("horario", width=150, anchor="center")
        self.tabela.column("sensor", width=150, anchor="center")
        self.tabela.column("valor", width=130, anchor="center")
        self.tabela.column("local", width=180, anchor="center")

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.tabela.yview
        )

        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def atualizar(self):

        self.tabela.delete(*self.tabela.get_children())

        registros = self.central.obter_historico()

        for registro in reversed(registros):

            timestamp = registro["timestamp"]

            if isinstance(timestamp, datetime):
                horario = timestamp.strftime("%d/%m/%Y %H:%M:%S")
            else:
                horario = str(timestamp).replace("T", " ")

            valor = registro["valor"]

            if isinstance(valor, bool):
                valor = "Detectado" if valor else "Sem movimento"
            else:
                valor = f"{valor:.2f}".replace(".", ",")

            unidade = registro["unidade"]

            self.tabela.insert(
                "",
                "end",
                values=(
                    horario,
                    registro["sensor"],
                    f"{valor} {unidade}".strip(),
                    registro["local"]
                )
            )
