from http.server import HTTPServer
from endpoints import Endpoints
from library.config import Config

Config.load()

PORTS = int(Config.get("http_ports"))
server = HTTPServer(("localhost", PORTS), Endpoints)
print("Play To Earn HTTP Server")
print("Version: 1.0")
print(f"\033[32mServer running on ports: {PORTS}\033[0m")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer closing by user (Ctrl+C). Shutting down...")
    server.shutdown()
    server.server_close()