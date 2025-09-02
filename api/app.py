from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/api/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    # в Codespaces нужно биндиться на 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
