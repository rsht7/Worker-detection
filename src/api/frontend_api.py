from flask import Flask, request, Response, jsonify
import json
import numpy as np
import io
from api.memory_store import MemoryStore
from utils.frontend_api_utils import convert_zone_json_to_array
from generated import service_pb2

def create_frontend_api(store: MemoryStore):
    app = Flask(__name__)

    @app.route("/zone", methods=["POST"])
    def receive_zone():
        data = request.get_json()
        if not data or "camera_id" not in data:
            return jsonify({"status": "error", "message": "Invalid input"}), 400

        camera_id = int(data["camera_id"])
        try:
            zone_array = convert_zone_json_to_array(data)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        formatted_zone_data = {
            "camera_id": camera_id,
            "zones": [
                {
                    "zone_id": 1,  # assuming single zone per POST for now
                    "zone_array": zone_array,
                    "rules": data.get("rules", [])
                }
            ]
        }

        store.set_zone_data(camera_id, formatted_zone_data)

        return jsonify({"status": "ok", "converted_zone": zone_array})

    @app.route("/alerts/<camera_id>")
    def alert_stream(camera_id):
        def event_stream():
            q = store.get_alert_stream(int(camera_id))
            while True:
                alert = q.get()
                yield f"data: {json.dumps(alert)}\n\n"

        return Response(event_stream(), content_type="text/event-stream")

    return app