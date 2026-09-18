import os
import json
import mimetypes
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PORT = 8100
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOLVES_FILE = os.path.join(BASE_DIR, "solves.json")
CHALLENGES_FILE = os.path.join(BASE_DIR, "challenges.json")


def load_json(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class CTFOfflineHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("", "/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/challenges")
            self.end_headers()
            return

        if path == "/challenges":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(BASE_DIR, "challenges.html"), "rb") as f:
                self.wfile.write(f.read())
            return

        if path == "/api/v1/challenges":
            challenges = load_json(CHALLENGES_FILE, [])
            solves = set(load_json(SOLVES_FILE, []))

            summary = []
            for ch in challenges:
                cid = ch["id"]
                is_solved = cid in solves
                summary.append(
                    {
                        "id": cid,
                        "type": "standard",
                        "name": ch["name"],
                        "value": ch["value"],
                        "solves": ch.get("solves", 0) + (1 if is_solved else 0),
                        "solved_by_me": is_solved,
                        "category": ch["category"],
                        "tags": ch.get("tags", []),
                        # Se eliminaron "template" y "script" para evitar 404
                    }
                )

            response_data = {"success": True, "data": summary}
            self.send_json(response_data)
            return

        if path.startswith("/api/v1/challenges/"):
            cid_str = path.split("/")[-1]
            try:
                cid = int(cid_str)
            except ValueError:
                cid = -1

            challenges = load_json(CHALLENGES_FILE, [])
            solves = set(load_json(SOLVES_FILE, []))

            found = next((ch for ch in challenges if ch["id"] == cid), None)
            if found:
                detail = dict(found)
                # Eliminar posibles campos que causan peticiones a archivos inexistentes
                detail.pop("template", None)
                detail.pop("script", None)
                detail["solved_by_me"] = cid in solves
                self.send_json({"success": True, "data": detail})
            else:
                self.send_json(
                    {"success": False, "errors": ["Challenge not found"]}, status=404
                )
            return

        if path in ("/api/v1/users/me", "/api/v1/teams/me"):
            self.send_json(
                {"success": True, "data": {"id": 1, "name": "Alumno", "score": 1000}}
            )
            return

        if path == "/api/v1/notifications":
            self.send_json({"success": True, "data": []})
            return

        if path == "/api/v1/shares":
            self.send_json({"success": True, "data": []})
            return

        # Ruta para Server-Sent Events (evita 404)
        if path == "/events":
            self.send_response(204)
            self.end_headers()
            return

        # Fallback to standard static file serving (CSS, JS, fonts, files)
        super().do_GET()

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Para cualquier endpoint de la API, respondemos 200 sin cuerpo
        if path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            return

        # Para archivos estáticos, delegamos al comportamiento normal
        super().do_HEAD()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/v1/challenges/attempt":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8", errors="ignore")
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            cid = payload.get("challenge_id")
            submission = payload.get("submission", "").strip()

            solves = set(load_json(SOLVES_FILE, []))
            if cid:
                solves.add(cid)
                save_json(SOLVES_FILE, list(solves))

            resp = {
                "success": True,
                "data": {
                    "status": "correct",
                    "message": f"¡Correcto! Flag '{submission}' enviada exitosamente.",
                },
            }
            self.send_json(resp)
            return

        self.send_json({"success": False, "errors": ["Endpoint not found"]}, status=404)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, CTFOfflineHandler)
    url = f"http://localhost:{PORT}/challenges"
    print("=" * 60)
    print(f" CTF FORENSE - SERVIDOR LOCAL OFFLINE ACTIVO")
    print(f" URL: {url}")
    print(f" Todos los retos y archivos están cargados localmente.")
    print(" Presiona Ctrl+C para detener el servidor.")
    print("=" * 60)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    run()
