
import tkinter

from .componentes import (
    criar_titulo,
    COR_FUNDO,
    COR_CARD,
    COR_TEXTO,
    COR_SECUNDARIA,
    COR_VERDE,
    COR_VERMELHO
)


class SensoresView(tkinter.Frame):

    def __init__(self, pai, central):
        super().__init__(pai, bg=COR_FUNDO)

        self.central = central
        self.labels = {}

        titulo = criar_titulo(
            self,
            "Sensores",
            "Informações e estado dos sensores"
        )
        titulo.pack(fill="x", pady=(0, 25))

        for sensor in central.obter_dados_sensores():

            card = tkinter.Frame(
                self,
                bg=COR_CARD,
                padx=20,
                pady=18,
                highlightbackground="#E2E8F0",
                highlightthickness=1
            )
            card.pack(fill="x", pady=6)

            tkinter.Label(
                card,
                text=sensor["nome"],
                font=("Arial", 12, "bold"),
                bg=COR_CARD,
                fg=COR_TEXTO
            ).pack(anchor="w")

            leitura = tkinter.Label(
                card,
                text="Aguardando leitura...",
                font=("Arial", 20, "bold"),
                bg=COR_CARD,
                fg="#2563EB"
            )
            leitura.pack(anchor="w", pady=8)

            status = tkinter.Label(
                card,
                text="Aguardando",
                font=("Arial", 10),
                bg=COR_CARD,
                fg=COR_SECUNDARIA
            )
            status.pack(anchor="w")

            limites = tkinter.Label(
                card,
                text=self.formatar_limites(sensor),
                font=("Arial", 9),
                bg=COR_CARD,
                fg=COR_SECUNDARIA
            )
            limites.pack(anchor="w", pady=(5, 0))

            self.labels[sensor["id"]] = {
                "leitura": leitura,
                "status": status,
                "limites": limites
            }

    @staticmethod
    def formatar_limites(sensor):

        if sensor["tipo"] == "movimento":
            return "Detecção de movimento"

        minimo = f"{sensor['minimo']:.2f}".replace(".", ",")
        maximo = f"{sensor['maximo']:.2f}".replace(".", ",")

        return (
            f"Limites: {minimo} a {maximo} "
            f"{sensor['unidade']}"
        )

    def atualizar(self):

        sensores = self.central.obter_dados_sensores()

        for sensor in sensores:

            elementos = self.labels[sensor["id"]]

            leitura = sensor["ultima_leitura"]

            if leitura is None:
                continue

            valor = leitura["valor"]

            if isinstance(valor, bool):
                valor_formatado = (
                    "Detectado" if valor else "Sem movimento"
                )
            else:
                valor_formatado = (
                    f"{valor:.2f}".replace(".", ",")
                )

            elementos["leitura"].config(
                text=f"{valor_formatado} {sensor['unidade']}".strip()
            )

            anomalia = leitura.get("anomalia", False)

            if anomalia:
                elementos["status"].config(
                    text="● Anomalia detectada",
                    fg=COR_VERMELHO
                )

            elif sensor["ativo"]:
                elementos["status"].config(
                    text="● Funcionando normalmente",
                    fg=COR_VERDE
                )

            else:
                elementos["status"].config(
                    text="● Sensor inativo",
                    fg=COR_VERMELHO
                )

            elementos["limites"].config(
                text=self.formatar_limites(sensor)
            )
