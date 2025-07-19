from datetime import datetime
from urllib.parse import parse_qs, urlparse

from library.database import Database

def getWallet(handler):
    parsed_path = urlparse(handler.path)
    query = parse_qs(parsed_path.query)

    from_header = handler.headers.get("from", "unknown") # Database table to get the wallet
    uniqueid = query.get("uniqueid", [None])[0] # Player unique id

    if not uniqueid:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(b"Error: Missing 'uniqueid' in query string")
        return

    if not uniqueid:
        print("----------------")
        print(f"\033[93m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-GetWallet] Missing methods\033[0m")
        print(f"\033[93m{uniqueid}\033[0m")
        print(f"\033[93m{from_header}\033[0m")
        print("----------------")
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(b"Error: Missing required fields")
        return
    
    print(f"\033----------------\033[0m")
    print(f"\033[92m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-GetWallet] Received\033[0m")
    print(f"\033[92m{uniqueid}\033[0m")
    print(f"\033[92m{from_header}\033[0m")
    print(f"\033----------------\033[0m")
    
    wallet = Database.GetWalletAddress(from_header, uniqueid)
    
    if wallet == None:
        handler.send_response(404)
        handler.end_headers()
        handler.wfile.write(b"")
    else:
        handler.send_response(200)
        handler.end_headers()
        handler.wfile.write(wallet.encode())