# src/api/frontend_api.py

from flask import Flask, request, Response, jsonify
import json


def create_frontend_api(store):
    app = Flask(__name__)

    @app.route("/zone", methods=["POST"])
    def receive_zone():
        data = request.get_json()
        if not data or "camera_id" not in data or "zones" not in data:
            return jsonify({"status": "error", "message": "Invalid input"}), 400


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

    @app.route("/alerts/<camera_id>")
    def alert_stream(camera_id):
        def event_stream():
            q = store.get_alert_stream(camera_id)
            while True:
                alert = q.get()
                yield f"data: {json.dumps(alert)}\n\n"

        return Response(event_stream(), content_type="text/event-stream")

    return app
