PROTOCCMD = protoc
POETRY_PATH = $(shell which poetry)

install_dev:
	$(POETRY_PATH) config virtualenvs.create false
	$(POETRY_PATH) lock
	$(POETRY_PATH) install --with=dev

install:
	$(POETRY_PATH) lock
	$(POETRY_PATH) install

src/stealthimfilestorage/proto/filestorage_pb2.py src/stealthimfilestorage/proto/filestorage_grpc.py: proto/filestorage.proto
	@mkdir -p src/stealthimfilestorage/proto
	python -m grpc_tools.protoc -Iproto --python_out=./src/stealthimfilestorage/proto --grpclib_python_out=./src/stealthimfilestorage/proto --mypy_out=./src/stealthimfilestorage/proto proto/filestorage.proto
	@echo "Rewrite File"
	@sed -i 's/import filestorage_pb2/from . import filestorage_pb2/g' ./src/stealthimfilestorage/proto/filestorage_grpc.py
	cp ./src/stealthimfilestorage/proto ./src/stimfstool/proto -r

proto: src/stealthimfilestorage/proto/filestorage_pb2.py src/stealthimfilestorage/proto/filestorage_grpc.py

build: proto
	poetry build

./bin/StealthIMFileStorage.docker.zst: $(GO_FILES) proto
	docker-compose build
	@mkdir -p ./bin
	docker save stealthimfilestorage-app > ./bin/StealthIMFileStorage.docker
	zstd ./bin/StealthIMFileStorage.docker -19
	@rm ./bin/StealthIMFileStorage.docker

build_docker: ./bin/StealthIMFileStorage.docker.zst

clean:
	@rm -rf ./src/stealthimfilestorage/proto
	@rm -rf ./bin
