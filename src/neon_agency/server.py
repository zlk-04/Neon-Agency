import argparse
import json
from importlib import resources
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from neon_agency.api import (
    handle_action_request,
    handle_reset_request,
    handle_state_request,
)
from neon_agency.cli import create_dialogue_provider
from neon_agency.simulation import create_default_street


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class NeonAgencyServer:
    def __init__(self, dialogue_provider=None):
        self.simulation = create_default_street()
        self.last_result = None
        self.dialogue_provider = dialogue_provider

    def state(self):
        return handle_state_request(self.simulation, last_result=self.last_result)

    def index_html(self):
        return (
            resources.files("neon_agency.web")
            .joinpath("index.html")
            .read_text(encoding="utf-8-sig")
        )

    def action(self, payload):
        response = handle_action_request(
            self.simulation,
            payload,
            dialogue_provider=self.dialogue_provider,
        )
        if response["status"] == 200:
            self.last_result = response["body"]["state"]["last_result"]
        return response

    def reset(self):
        response = handle_reset_request(create_default_street)
        self.simulation = response.pop("simulation")
        self.last_result = None
        return response


def create_handler(api_server):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in {"/", "/index.html"}:
                self._send_html(api_server.index_html())
                return
            if self.path == "/state":
                self._send_json(api_server.state())
                return
            self._send_json(_not_found(self.path))

        def do_POST(self):
            if self.path == "/action":
                payload = self._read_json()
                if payload is None:
                    self._send_json(
                        {
                            "status": 400,
                            "body": {
                                "error": "invalid_json",
                                "message": "Request body must be valid JSON.",
                            },
                        }
                    )
                    return
                self._send_json(api_server.action(payload))
                return
            if self.path == "/reset":
                self._send_json(api_server.reset())
                return
            self._send_json(_not_found(self.path))

        def log_message(self, format, *args):
            return

        def _read_json(self):
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length)
            try:
                return json.loads(raw_body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                return None

        def _send_json(self, response):
            body = json.dumps(response["body"], ensure_ascii=False).encode("utf-8")
            self.send_response(response["status"])
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_html(self, html):
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, dialogue_provider=None):
    api_server = NeonAgencyServer(dialogue_provider=dialogue_provider)
    httpd = ThreadingHTTPServer((host, port), create_handler(api_server))
    print(f"Neon Agency JSON API running at http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Neon Agency JSON API.")
    finally:
        httpd.server_close()


def main():
    parser = argparse.ArgumentParser(description="Run the Neon Agency local JSON API.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    run_server(args.host, args.port, dialogue_provider=create_dialogue_provider())


def _not_found(path):
    return {
        "status": 404,
        "body": {
            "error": "not_found",
            "message": f"Unknown endpoint: {path}",
        },
    }


if __name__ == "__main__":
    main()
