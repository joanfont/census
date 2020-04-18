.PHONY: build tests

build:
	docker-compose build

test:
	docker-compose run --rm --entrypoint=pytest api