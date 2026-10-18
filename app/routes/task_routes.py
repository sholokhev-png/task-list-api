from flask import Blueprint, request, jsonify
from app.db import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__)


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"details": "Invalid data"}), 400

    if not data.get("title") or not data.get("description"):
        return jsonify({"details": "Invalid data"}), 400

    task = Task.from_dict(data)

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    sort_order = request.args.get("sort")

    query = db.select(Task)

    if sort_order == "asc":
        query = query.order_by(Task.title.asc())

    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.execute(query).scalars().all()

    result = []

    for task in tasks:
        result.append(task.to_dict())

    return jsonify(result), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"details": "Task not found"}), 404

    return jsonify(task.to_dict()), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"details": "Task not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"details": "Invalid data"}), 400

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"details": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}