from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DATA_FILE = Path("/data/visitas.txt")


class VZetaHandler(BaseHTTPRequestHandler):
    def send_content(self, status, content_type, content):
        body = content.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_content(
                200,
                "application/json",
                '{"status":"ok","service":"myapp_container"}'
            )
            return

        if self.path != "/":
            self.send_content(
                404,
                "text/plain; charset=utf-8",
                "Recurso no encontrado"
            )
            return

        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with DATA_FILE.open("a", encoding="utf-8") as file:
            file.write(f"{datetime.now().isoformat()}\n")

        total = len(
            DATA_FILE.read_text(encoding="utf-8").splitlines()
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>VZeta</title>
        </head>
        <body>
            <h1>VZeta</h1>
            <h2>Infraestructura de Aplicaciones</h2>
            <p>Aplicación web ejecutada en Docker.</p>
            <p>Visitas registradas: {total}</p>
        </body>
        </html>
        """

        self.send_content(
            200,
            "text/html; charset=utf-8",
            html
        )


server = HTTPServer(("0.0.0.0", 5000), VZetaHandler)

print("Aplicación VZeta iniciada en el puerto 5000", flush=True)

server.serve_forever()
