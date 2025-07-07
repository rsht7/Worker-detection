all: build

build:
	@echo "no build command"

generate-proto:
	@echo "generating from proto file..."
	@python -m grpc_tools.protoc -Isrc/proto --python_out=./src/generated --pyi_out=./src/generated --grpc_python_out=./src/generated src/proto/service.proto
	@sed -i 's/^import service_pb2/from . import service_pb2/' src/generated/service_pb2_grpc.py

start-api:
	@echo "starting api..."
	PYTHONPATH=src python src/api/main.py
