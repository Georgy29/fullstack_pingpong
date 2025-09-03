from flask import Flask, request, jsonify
from flask_cors import CORS

TODOS = [{"id": 1, "title": "learn git", "done": True}]

app = Flask(__name__)
CORS(app)

@app.get("/api/ping")
def ping():
    return "pong"

@app.get("/api/todos")
def list_todos():
    return jsonify(TODOS)

@app.post("/api/todos")
def create_todo():
    data = request.get_json(force=True)
    new_id = max([t["id"] for t in TODOS] or [0]) + 1
    todo = {"id": new_id, "title": data.get("title","").strip(), "done": False}
    TODOS.append(todo)
    return jsonify(todo), 201

@app.patch("/api/todos/<int:todo_id>")
def toggle_todo(todo_id):
    for t in TODOS:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            return jsonify(t)
    return jsonify({"error":"not found"}), 404

@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    global TODOS
    before = len(TODOS)
    TODOS = [t for t in TODOS if t["id"] != todo_id]
    return ("", 204) if len(TODOS) < before else (jsonify({"error":"not found"}), 404)

if __name__ == "__main__":
    # в Codespaces нужно биндиться на 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
