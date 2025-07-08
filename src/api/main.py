import grpc
import threading
from concurrent import futures
from api.frontend_api import create_frontend_api
from api.memory_store import MemoryStore
from api.grpc_bridge import GRPCBridge
from generated import service_pb2_grpc

def run_grpc_server(store: MemoryStore):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SurveillanceServicer_to_server(GRPCBridge(store), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("✅ gRPC server running on port 50051")
    server.wait_for_termination()

def run_http_server(store: MemoryStore):
    app = create_frontend_api(store)
    print("🌐 Flask server running on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000, threaded=True)

if __name__ == "__main__":
    store = MemoryStore()

    grpc_thread = threading.Thread(target=run_grpc_server, args=(store,), daemon=True)
    grpc_thread.start()

    run_http_server(store)
