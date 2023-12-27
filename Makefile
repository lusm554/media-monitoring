include .env

pull:
	docker pull $(DOCKER_USER_NAME)/$(CONTAINER_NAME):latest
run: pull
	docker run -d --env-file .env $(DOCKER_USER_NAME)/$(CONTAINER_NAME):latest

build:
	docker build --platform=linux/amd64 -t $(DOCKER_USER_NAME)/$(CONTAINER_NAME) .
push: build
	docker push $(DOCKER_USER_NAME)/$(CONTAINER_NAME)
deploy: push
	$(shell sed 's/=.*/=/' .env > .env.example)
	# deploy here 

all: deploy

