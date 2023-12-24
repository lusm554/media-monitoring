include .env

create:
	yc serverless container create --name $(SERVERLESS_CONTAINER_NAME)
	yc serverless container allow-unauthenticated-invoke --name  $(SERVERLESS_CONTAINER_NAME)

create_gw_spec:
	$(shell sed "s/SERVERLESS_CONTAINER_ID/${SERVERLESS_CONTAINER_ID}/;s/SERVICE_ACCOUNT_ID/${SERVICE_ACCOUNT_ID}/" api-gw.yaml.example > api-gw.yaml)
create_gw: create_gw_spec
	yc serverless api-gateway create --name $(SERVERLESS_CONTAINER_NAME) --spec api-gw.yaml

webhook_info:
	curl --request POST --url "https://api.telegram.org/bot$(TELEGRAM_TOKEN)/getWebhookInfo"
webhook_delete:
	curl --request POST --url "https://api.telegram.org/bot$(TELEGRAM_TOKEN)/deleteWebhook"
webhook_create: webhook_delete
	curl --request POST --url "https://api.telegram.org/bot$(TELEGRAM_TOKEN)/setWebhook" --header 'content-type: application/json' --data "{\"url\": \"$(SERVERLESS_APIGW_URL)\"}"


build: webhook_create
	docker build --platform=linux/amd64 -t cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME) .
push: build
	docker push cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME)
deploy: push
	$(shell sed 's/=.*/=/' .env > .env.example)
	yc serverless container revision deploy \
		--container-name $(SERVERLESS_CONTAINER_NAME) \
		--image 'cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME):latest' \
		--service-account-id $(SERVICE_ACCOUNT_ID) \
	  --environment='$(shell awk '{q=p;p=$$0}NR>1{print q}END{ORS = ""; print p}' .env | tr '\n' ',')' \
		--execution-timeout $(SERVERLESS_CONTAINER_EXEC_TIMEOUT) \
		--core-fraction 100 \
		--memory 256MB \
		--concurrency 3 \
		--cores 4

all: deploy

