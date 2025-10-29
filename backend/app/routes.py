# backend/app/routes.py
from flask import Blueprint, request, jsonify
from .tasks import generate_itinerary_task
from celery.result import AsyncResult

main = Blueprint('main', __name__)

@main.route('/itinerary', methods=['POST'])
def create_itinerary():
    data = request.get_json()
    interests = data.get('interests')
    duration = data.get('duration')

    if not interests or not duration:
        return jsonify({"error": "Missing interests or duration"}), 400

    # Start the background task
    task = generate_itinerary_task.delay(interests, duration)

    # Return the task ID to the client
    return jsonify({"task_id": task.id}), 202

@main.route('/itinerary/result/<task_id>', methods=['GET'])
def get_result(task_id):
    task_result = AsyncResult(task_id, app=generate_itinerary_task.app)

    if task_result.ready():
        if task_result.successful():
            result = task_result.get()
            return jsonify(result)
        else:
            return jsonify({"status": "FAILURE", "error": str(task_result.info)}), 500
    else:
        return jsonify({"status": "PENDING"}), 202