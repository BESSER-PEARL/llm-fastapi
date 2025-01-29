# docker-llm
A Dockerizable FastAPI to deploy a HuggingFace LLM


## Instructions

First, build the docker image:

```shell
docker build -t llm-fastapi .
```

Second, create the container with docker-compose. Make sure to set the LLM name (HuggingFace model id) in the docker-compose.yml.

Optionally, set your HuggingFace token (necessary for some LLMs that need authentication).

You can also change the port (left-side port)

```shell
docker-compose up --build
```

You can send HTTP requests through the `localhost:<your-port>/docs` page