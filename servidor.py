import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread


class ServidorSensores:
    def __init__(self, central, host="0.0.0.0", porta=5000):
        self.central = central
        self.host = host
        self.porta = porta
        self.servidor = None
        self.thread = None

    def iniciar(self):
        central = self.central

        class RequisicaoHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path != "/leituras":
                    self.send_error(404, "Rota nao encontrada")
                    return

                try:
                    tamanho = int(self.headers.get("Content-Length", 0))

                    if tamanho <= 0 or tamanho > 4096:
                        self.send_error(400, "Tamanho de requisicao invalido")
                        return

                    corpo = self.rfile.read(tamanho)
                    dados = json.loads(corpo.decode("utf-8"))

                    if not isinstance(dados, dict):
                        raise ValueError("JSON invalido")

                    temperatura = dados["temperatura"]
                    umidade = dados["umidade"]
                    movimento = dados["movimento"]

                    if (
                        isinstance(temperatura, bool)
                        or not isinstance(temperatura, (int, float))
                        or isinstance(umidade, bool)
                        or not isinstance(umidade, (int, float))
                        or not isinstance(movimento, bool)
                    ):
                        raise ValueError("Tipos de dados invalidos")

                    central.receber_leituras(dados)
                    resposta = {
                        "status": "sucesso",
                        "mensagem": "Leituras recebidas"
                    }
                    self.enviar_resposta(200, resposta)
                except (KeyError, ValueError, json.JSONDecodeError) as erro:
                    self.enviar_resposta(400, {
                        "status": "erro",
                        "mensagem": str(erro)
                    })
                except Exception as erro:
                    print(f"Erro ao processar leitura: {erro}")
                    self.enviar_resposta(500, {
                        "status": "erro",
                        "mensagem": "Erro interno do servidor"
                    })

            def enviar_resposta(self, codigo, dados):
                resposta = json.dumps(dados).encode("utf-8")
                self.send_response(codigo)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resposta)))
                self.end_headers()
                self.wfile.write(resposta)

            def log_message(self, formato, *args):
                print(f"[ESP8266] {formato % args}")

        self.servidor = ThreadingHTTPServer(
            (self.host, self.porta),
            RequisicaoHandler
        )
        self.thread = Thread(
            target=self.servidor.serve_forever,
            daemon=True
        )
        self.thread.start()
        print(f"Servidor iniciado em http://{self.host}:{self.porta}")

    def parar(self):
        if self.servidor:
            self.servidor.shutdown()
            self.servidor.server_close()
            self.servidor = None

            print("Servidor encerrado.")
