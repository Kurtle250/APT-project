#################################################
# Makefile to build docker images
#
# EXAMPLE RUN COMMANDS
# make build run
#################################################
# Top level vars
PROJECT_DIR?=$(shell pwd)
DOCKER_DIR:=$(PROJECT_DIR)/.docker
include .env

#################################################
# HELPERS
help:
	@echo "++   PROJECT COMMANDS"
	@echo "++ 	make build"
	@echo "++ 	make run"
	@echo "++   VARIABLES"
	@echo "++	PROJECT_NAME: 	$(PROJECT_NAME)"
	@echo "++	IMAGE_PREFIX: 	$(IMAGE_PREFIX)"
	@echo "++	TZ:           	$(TZ)"

#################################################
# GENERAL BUILD COMMANDS
build: network build_db
run: run_db

network:
	docker network create \
      --driver=bridge \
      --subnet="$(SUBNET_BASE).0/24" \
      --gateway="$(SUBNET_BASE).1" \
      $(PROJECT_NAME)_server || echo "Network alive"

#################################################
# DOCKER PROJECT COMMANDS
# BUILD COMMANDS

build_db:
	docker buildx build -t $(REGISTRY_URL)/$(IMAGE_PREFIX)-database $(DOCKER_DIR)/database --build-arg DB_USER=$(DB_USER) --build-arg DB_PWD=$(DB_PWD)

# RUN COMMANDS
run_db: network
	docker run -d --name database \
	    --net=$(PROJECT_NAME)_server \
	    --ip="$(SUBNET_BASE).2" \
      	-p 7000:7000 \
      	-p 7001:7001 \
      	-p 7199:7199 \
      	-p 9042:9042 \
      	-p 9160:9160 \
      	-v "/etc/localtime:/etc/localtime:ro" \
	    --user=0 \
	     $(REGISTRY_URL)/$(IMAGE_PREFIX)-database

# CONTAINER STOP & CLEAN UP COMMANDS
kill:
	docker kill $(shell docker ps -q) || echo "no containers are running ... ready to go!"

clean: kill
	docker container prune -f;
	docker network prune -f;
	docker volume prune -f;

clean_all: clean
	docker system prune -af;

#################################################
# DEVELOPMENT HELPERS


# DATABASE MANAGEMENT
docker_login:
	docker login
image_push:
	docker push "docker.io/$(REGISTRY_URL)/$(IMAGE_PREFIX)-database"
db_login:
	@echo "---- View .docker/database/README.md for useful commands --- "
	@echo ""
	docker exec -it database bash -c "cqlsh -u $(DB_USER) -p $(DB_PWD)"
database_clear:
	docker exec -it database bash -c "python3 database/database_clear.py $(ip)"
database_load:
	docker exec -it database bash -c "python3 database/db/file2db.py decoder $(number_rows)"

	# FILE PERMISSIONS
files:
	chown -R ${USER}:${USER} data
	chmod -R 777 data