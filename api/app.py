from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta
import os

from .db import db
from .models import User, Todo


def create_app():
    app = Flask(__name__)

    # --- CONFIG ---
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
    # optional: set access token lifetime
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=4)

    # CORS: strict in prod, open in dev
    frontend_origin = os.environ.get("FRONTEND_ORIGIN")  # e.g. https://your-site.netlify.app
    if frontend_origin:
        CORS(app, origins=[frontend_origin])
    else:
        CORS(app)  # dev

    # --- INIT ---
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    @app.get("/api/todos")
    @jwt_required()  # <-- без токена 401
    def get_todos():
        uid = get_jwt_identity()  # <-- id текущего пользователя из JWT
        items = Todo.query.filter_by(user_id=uid).order_by(Todo.id.asc()).all()
        return jsonify([t.to_dict() for t in items])

    @app.post("/api/todos")
    @jwt_required()
    def add_todo():
        uid = get_jwt_identity()
        data = request.get_json(force=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title is required"}), 400
        todo = Todo(title=title, done=False, user_id=uid)  # <-- привязка к пользователю
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201

    @app.patch("/api/todos/<int:todo_id>")
    @jwt_required()
    def toggle_todo(todo_id: int):
        uid = get_jwt_identity()
        # В SQLAlchemy 2.0 предпочтительнее так:
        todo = db.session.get(Todo, todo_id)   # вместо Todo.query.get(...)
        if not todo or todo.user_id != uid:    # проверяем владельца
            return jsonify({"error": "not found"}), 404
        todo.done = not todo.done
        db.session.commit()
        return jsonify(todo.to_dict())

    @app.delete("/api/todos/<int:todo_id>")
    @jwt_required()
    def delete_todo(todo_id: int):
        uid = get_jwt_identity()
        todo = db.session.get(Todo, todo_id)
        if not todo or todo.user_id != uid:
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