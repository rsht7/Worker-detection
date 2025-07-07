from api.memory_store import MemoryStore
from generated import service_pb2, service_pb2_grpc
from api.img_save import save_alert_image


class GRPCBridge(service_pb2_grpc.SurveillanceServicer):
    def __init__(self, store: MemoryStore):
        self.store = store

    def GetZoneData(self, request, context):
        data = self.store.get_zone_data(request.camera_id)
        if not data:
            return service_pb2.ZoneData(camera_id=request.camera_id, zones=[])

        return service_pb2.ZoneData(**data)

    def SendAlert(self, request, context):
        print(f"[gRPC] Alert received: {request.camera_id}, {request.alert_type}")

        img_path = save_alert_image(request.timestamp, request.camera_id, request.image)
        alert_dict = {
            "camera_id": request.camera_id,
            "zone_id": request.zone_id,
            "alert_type": request.alert_type,
            "rules": request.rules,
            "confidence": request.confidence,
            "timestamp": request.timestamp,
            # TODO: store image first and send path to alert
            "image": img_path,
        }
        # TODO: store in sqlite
        self.store.push_alert(request.camera_id, alert_dict)
        return service_pb2.Ack(success=True)
