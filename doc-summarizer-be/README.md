### Setting up FastAPI

- Run qdrant and mongodb locally

  ```bash
  docker compose up qdrant
  docker compose up mongodb
  ```

- Install the required packages with poetry:

  ```bash
  poetry install
  poetry run uvicorn app.main:app
  ```
