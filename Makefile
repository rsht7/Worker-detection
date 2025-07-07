all: build

build:
	@echo "no build command"
generate-proto:
	@echo "generating from proto file..."
	@python -m grpc_tools.protoc -I./src/proto --python_out=./src/generated --pyi_out=./src/generated --grpc_python_out=./src/generated src/proto/service.proto
