import tkinter
from tkinter import messagebox
from datetime import datetime


class ConfiguracoesView(tkinter.Frame):
    def __init__(self, pai, central):
        super().__init__(pai, bg="#F1F5F9")
        self.central = central
        self.campos = {}
        self.criar_interface()

    def criar_interface(self):
        tkinter.Label(self,
            text="Configurações",
            font=("Arial", 24, "bold"),
            fg="#1E293B",
            bg="#F1F5F9"
        ).pack(anchor="w", pady=(0, 25))
        configuracoes = self.central.configuracoes
        formulario = tkinter.Frame(
            self,
            bg="white",
            padx=25,
            pady=25
        )
        formulario.pack(fill="x", anchor="n")
        self.criar_secao(formulario, "Temperatura",
            [
                ("temperatura_minima", "Temperatura mínima (°C)"),
                ("temperatura_maxima", "Temperatura máxima (°C)")
            ],
            configuracoes
        )

        self.criar_secao(formulario, "Umidade",
            [
                ("umidade_minima", "Umidade mínima (%)"),
                ("umidade_maxima", "Umidade máxima (%)")
            ],
            configuracoes
        )

        self.criar_secao(formulario, "Movimento",
            [
                (
                    "horario_movimento_inicio",
                    "Horário inicial permitido (HH:MM)"
                ),
                (
                    "horario_movimento_fim",
                    "Horário final permitido (HH:MM)"
                )
            ],
            configuracoes
        )

        self.criar_secao(formulario, "Monitoramento",
            [
                (
                    "intervalo_coleta",
                    "Intervalo entre coletas (segundos)"
                )
            ],
            configuracoes
        )

        tkinter.Button(self,
            text="Salvar configurações",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#16A34A",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.salvar
        ).pack(anchor="w", pady=20)

    def criar_secao(self, pai, titulo, campos, configuracoes):
        secao = tkinter.Frame(
            pai,
            bg="white"
        )
        secao.pack(fill="x", pady=(0, 20))
        tkinter.Label(
            secao,
            text=titulo,
            font=("Arial", 13, "bold"),
            fg="#1E293B",
            bg="white"
        ).pack(anchor="w", pady=(0, 10))

        for chave, descricao in campos:
            linha = tkinter.Frame(
                secao,
                bg="white"
            )
            linha.pack(fill="x", pady=5)
            tkinter.Label(
                linha,
                text=descricao,
                font=("Arial", 10),
                fg="#475569",
                bg="white",
                width=35,
                anchor="w"
            ).pack(side="left")
            entrada = tkinter.Entry(
                linha,
                font=("Arial", 10),
                width=15,
                relief="solid",
                bd=1
            )

            entrada.pack(side="left")
            entrada.insert(
                0,
                str(configuracoes[chave])
            )
            self.campos[chave] = entrada

    def salvar(self):
        try:
            temperatura_minima = float(self.campos["temperatura_minima"].get().replace(",", "."))
            temperatura_maxima = float(self.campos["temperatura_maxima"].get().replace(",", "."))
            umidade_minima = float(self.campos["umidade_minima"].get().replace(",", "."))
            umidade_maxima = float(self.campos["umidade_maxima"].get().replace(",", "."))

            horario_inicio = self.campos["horario_movimento_inicio"].get()

            horario_fim = self.campos["horario_movimento_fim"].get()

            intervalo_coleta = int(self.campos["intervalo_coleta"].get())

            if temperatura_minima >= temperatura_maxima:
                raise ValueError("A temperatura mínima deve ser menor que a máxima.")
            if umidade_minima >= umidade_maxima:
                raise ValueError("A umidade mínima deve ser menor que a máxima.")
            
            datetime.strptime(horario_inicio, "%H:%M")
            datetime.strptime(horario_fim, "%H:%M")

            if intervalo_coleta <= 0:
                raise ValueError("O intervalo de coleta deve ser maior que zero.")
            
            self.central.atualizar_configuracoes(
                temperatura_minima,
                temperatura_maxima,
                umidade_minima,
                umidade_maxima,
                horario_inicio,
                horario_fim,
                intervalo_coleta
            )

            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")

        except ValueError as erro:

            messagebox.showerror("Erro nas configurações", str(erro))

        except OSError as erro:

            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar as configurações:\n{erro}")
