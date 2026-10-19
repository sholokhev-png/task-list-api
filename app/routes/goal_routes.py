from flask import Blueprint, request, jsonify
from ..db import db
from ..models.goal import Goal

goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["POST"])
def create_goal():
    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201


@goals_bp.route("/goals", methods=["GET"])
def get_goals():
    goals = db.session.execute(db.select(Goal)).scalars().all()

    goals_list = []

    for goal in goals:
        goals_list.append(goal.to_dict())

    return jsonify(goals_list), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if goal is None:
        return jsonify({"details": "Goal not found"}), 404

    return jsonify(goal.to_dict()), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if goal is None:
        return jsonify({"details": "Goal not found"}), 404

    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400

    goal.title = request_body["title"]
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@goals_bp.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if goal is None:
        return jsonify({"details": "Goal not found"}), 404

    db.session.delete(goal)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}
