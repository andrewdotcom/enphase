docker:
	docker build --no-cache --tag enphase --file DockerFile .

gen_requirements:
	pip3 freeze > requirements.txt

run:
	docker run -e PYTHONUNBUFFERED=1 -v ${HOME}/Src/experiments/enphase/data:/enphase/data enphase

all: gen_requirements docker run