from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# Routes
from routes.get_balance import getBalance
from routes.get_balanceraw import getBalanceRaw
from routes.get_wallet import getWallet
from routes.increment import increment
from routes.update_wallet import updateWallet
from routes.register import register

class Endpoints(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path        

        if path == "/":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")
        elif path == "/getwallet":
            getWallet(self)
        elif path == "/getbalance":
            getBalance(self)
        elif path == "/getbalanceraw":
            getBalanceRaw(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")

    def do_POST(self):
        if self.path == "/register":
            register(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")

    def do_PUT(self):
        if self.path == "/increment":
            increment(self)
        elif self.path == "/updatewallet":
            updateWallet(self)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")