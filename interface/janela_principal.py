import tkinter
from .dashboard import Dashboard
from .sensores_view import SensoresView
from .localizacoes_view import LocalizacoesView
from .historico_view import HistoricoView
from .alertas_view import AlertasView
from .configuracoes_view import ConfiguracoesView


class JanelaPrincipal:
    def __init__(self, central, servidor):
        self.central = central
        self.servidor = servidor
        self.janela = tkinter.Tk()
        self.janela.title("SenseTrack")
        self.janela.geometry("1100x700")
        self.janela.minsize(850, 550)
        self.janela.configure(bg="#F1F5F9")
        self.tela_atual = None
        self.atualizacao_agendada = None
        self.criar_layout()
        self.mostrar_tela(Dashboard)
        self.agendar_atualizacao()
        self.janela.protocol(
            "WM_DELETE_WINDOW",
            self.encerrar
        )

    def criar_layout(self):
        self.menu = tkinter.Frame(
            self.janela,
            bg="#1E293B",
            width=220
        )
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)
        tkinter.Label(
            self.menu,
            text="SenseTrack",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1E293B"
        ).pack(pady=(30, 5))
        tkinter.Label(
            self.menu,
            text="MONITORAMENTO",
            font=("Arial", 8, "bold"),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(pady=(0, 30))
        botoes = [
            ("Dashboard", Dashboard),
            ("Sensores", SensoresView),
            ("Localizações", LocalizacoesView),
            ("Histórico", HistoricoView),
            ("Alertas", AlertasView),
            ("Configurações", ConfiguracoesView)
        ]

        for nome, tela in botoes:
            botao = tkinter.Button(
                self.menu,
                text=nome,
                font=("Arial", 11),
                fg="#E2E8F0",
                bg="#1E293B",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=25,
                pady=14,
                cursor="hand2",
                command=lambda t=tela: self.mostrar_tela(t)
            )
            botao.pack(fill="x")

        self.conteudo = tkinter.Frame(self.janela,
            bg="#F1F5F9"
        )
        self.conteudo.pack(
            side="right",
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

    def mostrar_tela(self, tela):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        nova_tela = tela(self.conteudo, self.central)
        nova_tela.pack(fill="both", expand=True)
        self.tela_atual = nova_tela
        self.atualizar_tela()

    def atualizar_tela(self):
        if self.tela_atual and hasattr(
            self.tela_atual,
            "atualizar"
        ):
            self.tela_atual.atualizar()

    def agendar_atualizacao(self):
        self.atualizacao_agendada = self.janela.after(
            1000,
            self.executar_atualizacao
        )

    def executar_atualizacao(self):
        self.atualizar_tela()
        self.agendar_atualizacao()

    def encerrar(self):
        if self.atualizacao_agendada:
            self.janela.after_cancel(self.atualizacao_agendada)

        self.servidor.parar()
        print("\nMonitoramento encerrado.")
        self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()
