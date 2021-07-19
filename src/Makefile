docker:
	docker build --no-cache --tag enphase --file DockerFile .

gen_requirements:
	pip3 freeze > requirements.txt

run:
	docker run --rm -e PYTHONUNBUFFERED=1 -v ${HOME}/Dev/enphase/data:/enphase/data enphase

refresh: docker run

all: gen_requirements docker run
