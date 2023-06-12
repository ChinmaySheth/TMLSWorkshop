# TMLSWorkshopFrontend

## Purpose

This repository contains a basic application which can be used for inspiration to deploy your own LLM. It is meant to serve advisors who want to use natural language to gather information about banking clients based on:
- First name
- Net worth
- Location
- Company

## Technical Design

Both the frontend and backend contain Dockerfiles which can easily be built once [Docker](https://docs.docker.com/engine/install/) is installed. You must first build the docker containers using the instructions below and then run each docker container.

### FRONTEND

#### Building the Docker Container
```cd tmls-workshop-frontend && docker build -t tmls-workshop-frontend```

#### Running the frontend in a Docker container:
```docker run -d -p 127.0.0.1:8400:80 tmls-workshop-frontend:latest```

#### Building on top of the frontend
If you want to continue to build on top of the frontend then you will have to install [Angular](https://angular.io/guide/setup-local) and [NodeJS](https://nodejs.org/en/download).


### BACKEND
Please don't forget to add a .env file to tmls-backend-workshop containing the following contents:
```OPENAI_API_KEY=""``` 

```OPENAI_API_KEY``` should be populated with your [OpenAI Key](https://openai.com/). The application's backend will be unable to connect to the OpenAI API without this .env file. Additionally, if the pipenv shell has already been launched, please make sure that you restart it everytime you update the .env file.

#### Building the Docker Container
```cd tmls-workshop-backend && docker build -t tmls-workshop-backend```

#### Running the backend in a Docker container:
```docker run tmls-workshop-backend uvicorn main:app --host 127.0.0.1 --port 80```

#### Building on top of the backend
If you want to continue to build on top of the backend then you will have to install [Python](https://www.python.org/downloads/) and [Pipenv](https://pipenv.pypa.io/en/latest/installation/).
