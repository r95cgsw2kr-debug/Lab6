from http.server import BaseHTTPRequestHandler, HTTPServer 
import json 
import time 
from urllib.parse import urlparse

HOST = "127.0.0.1" 
PORT = 8000

USERS = { 
    "token_user_a": {"id": 1, "name": "User A", "role": "user"}, 
    "token_user_b": {"id": 2, "name": "User B", "role": "user"}, 
    "token_admin": {"id": 3, "name": "Admin", "role": "admin"} 
}

ORDERS = { 
    "1001": {"id": 1001, "user_id": 1, "product": "Laptop", "amount": 1200}, 
    "1002": {"id": 1002, "user_id": 2, "product": "Phone", "amount": 500} 
}

class APIHandler(BaseHTTPRequestHandler): 
    def send_json(self, status, data): 
        body = json.dumps(data).encode("utf-8") 
        self.send_response(status) 
        self.send_header("Content-Type", "application/json") 
        self.send_header("Content-Length", str(len(body))) 
        self.end_headers() 
        self.wfile.write(body)

    def get_user(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth.replace("Bearer ", "", 1)
        return USERS.get(token)

    def do_GET(self):
        path = urlparse(self.path).path
        user = self.get_user()

        if path == "/api/profile":
            if user is None:
                return self.send_json(401, {"error": "Unauthorized"})
            return self.send_json(200, {
                "id": user["id"],
                "name": user["name"],
                "role": user["role"]
           })

        if path == "/api/admin":
            if user is None:
                return self.send_json(401, {"error": "Unauthorized"})
            if user["role"] != "admin":
                return self.send_json(403, {"error": "Forbidden"})
            return self.send_json(200, {"message": "Admin access granted"})

        if path.startswith("/api/orders/"):
            if user is None:
                return self.send_json(401, {"error": "Unauthorized"})

            order_id = path.split("/")[-1]
            order = ORDERS.get(order_id)

            if order is None:
                return self.send_json(404, {"error": "Not found"})

            if order["user_id"] != user["id"] and user["role"] != "admin":
                return self.send_json(403, {"error": "Forbidden"})

            return self.send_json(200, order)

        if path == "/api/slow":
            time.sleep(5)
            return self.send_json(200, {"message": "Response delayed"})

        if path == "/api/products":
            return self.send_json(200, {
                "products": ["Laptop", "Phone", "Tablet"]
           })

        return self.send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), APIHandler)
    print(f"Test API running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()