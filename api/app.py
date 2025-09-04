from flask import Flask, request, jsonify
from flask_cors import CORS
from .db import db
from .models import Todo

def create_app():
    app = Flask(__name__)
    CORS(app)  # в проде сузишь origins
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/api/ping")
    def ping():
        return "pong"

    @app.get("/api/todos")
    def get_todos():
        items = Todo.query.order_by(Todo.id.asc()).all()
        return jsonify([t.to_dict() for t in items])

    @app.post("/api/todos")
    def add_todo():
        data = request.get_json(force=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title is required"}), 400
        todo = Todo(title=title, done=False)
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201

    @app.patch("/api/todos/<int:todo_id>")
    def toggle_todo(todo_id: int):
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({"error": "not found"}), 404
        todo.done = not todo.done
        db.session.commit()
        return jsonify(todo.to_dict())

    @app.delete("/api/todos/<int:todo_id>")
    def delete_todo(todo_id: int):
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({"error": "not found"}), 404
        db.session.delete(todo)
        db.session.commit()
        return ("", 204)

    return app

# локальный запуск для dev
if __name__ == "__main__":
    import os
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Codespaces проксирует этот порт
    app.run(host="0.0.0.0", port=port, debug=True)