FROM python:3.11-slim

RUN pip install poetry==1.6.1

WORKDIR /app
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./README.md ./poetry.lock* ./
RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./src ./src

RUN poetry install --no-interaction --no-ansi

CMD [ "python3", "src/app.py"]