from flask import Flask, request, Response, jsonify
import json

import numpy as np
import io
from api.memory_store import MemoryStore
from utils.frontend_api_utils import convert_zone_json_to_array
from generated import service_pb2

def create_frontend_api(store: MemoryStore):

from utils.constants import Rule


def create_frontend_api(store):

    app = Flask(__name__, static_url_path="/images", static_folder="./static/images")

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

        # convert data to following format
        # {
        #   101: {  # camera_id (int)
        #     "camera_id": 101,
        #     "zones": [
        #       {
        #         "zone_id": 1,
        #         "numpy_mask": b'...',  # serialized using np.save(..., allow_pickle=False)
        #         "rules": [0, 1]
        #       },
        #       {
        #         "zone_id": 2,
        #         "numpy_mask": b'...',  # another zone
        #         "rules": [2]
        #       }
        #     ]
        #   },
        # }

        # store.set_zone_data(CAMERAID, CHANGED DATA)
        return jsonify({"status": "ok", "message": "Zone data stored"})


    @app.route("/rules", methods=["GET"])
    def get_rules():
        rules = [
            {"ruleID": rule.value, "name": rule.name.replace("_", " ").title()}
            for rule in Rule
        ]
        return jsonify(rules)

    @app.route("/alerts/<camera_id>")
    def alert_stream(camera_id):
        def event_stream():
            q = store.get_alert_stream(int(camera_id))
            while True:
                alert = q.get()
                yield f"data: {json.dumps(alert)}\n\n"

        return Response(event_stream(), content_type="text/event-stream")

    return app