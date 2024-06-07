include .env

gitpull:
	git pull --rebase
pull: gitpull
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

develop_run:
	docker build --platform=linux/amd64 -t develop .
	docker run -d --env dev=1 --env-file .dev_env develop

prod_run:
	docker build --platform=linux/amd64 -t develop .
	docker run -d --env-file .env develop

all: deploy
