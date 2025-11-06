from granian import Granian
from app.main import asgi_app

if __name__ == "__main__":
    server = Granian(target=asgi_app, interface="asgi", workers=1)
    server.serve("127.0.0.1:5000")