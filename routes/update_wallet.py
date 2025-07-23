from datetime import datetime
import json

from library.database import Database

def updateWallet(handler):
    content_length = int(handler.headers.get('Content-Length', 0))
    if content_length == 0:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(b"Error: Content-Length is missing or body empty")
        return
    
    body = handler.rfile.read(content_length) if content_length > 0 else b""
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(b"Error: Invalid JSON")
        return

    from_header = handler.headers.get("from", "unkown") # Database table to update wallet
    wallet = data.get("walletaddress") # Player wallet
    uniqueid = data.get("uniqueid") # Player unique id

    if not wallet or not uniqueid:
        print("----------------")
        print(f"\033[93m[{datetime.now().strftime('%H:%M:%S/%d/%m/%Y')}-UpdateWallet] Missing methods\033[0m")
        print(f"\033[93m{wallet}\033[0m")
        print(f"\033[93m{uniqueid}\033[0m")
        print(f"\033[93m{from_header}\033[0m")
        print("----------------")
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(b"Error: Missing required fields")
        return
    
    print("----------------")
    print(f"\033[92m[{datetime.now().strftime('%H:%M:%S/%d/%m/%Y')}-UpdateWallet] Received\033[0m")
    print(f"\033[92m{wallet}\033[0m")    
    print(f"\033[92m{uniqueid}\033[0m")
    print(f"\033[92m{from_header}\033[0m")
    print("----------------")
    
    if Database.UpdateWalletAddress(from_header, wallet, uniqueid):
        handler.send_response(200)
        handler.end_headers()
        handler.wfile.write(b"")
    else:
        handler.send_response(500)
        handler.end_headers()
        handler.wfile.write(b"Error: Database error")