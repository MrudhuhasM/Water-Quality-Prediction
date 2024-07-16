FROM python:3.12-slim AS build

RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/poetry \
    && poetry config virtualenvs.create false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -u 1000 -m appuser
WORKDIR /home/appuser/src

COPY ./pyproject.toml ./poetry.lock ./

COPY . .

RUN poetry install --no-root --no-dev \
    && poetry build \
    && pip install dist/*.whl \
    && rm -rf dist && rm -rf build


ENV DATA_PATH='/home/appuser/src/waterquality/data'
ENV MODEL_PATH='/home/appuser/src/waterquality/models'
ENV MODEL_NAME='waterquality_model.pkl'
ENV DATA_FILE_NAME='data.csv'
ENV HOST='0.0.0.0'
ENV PORT=8000

RUN chmod +x /home/appuser/src/waterquality/pipeline.py && \
    mkdir -p /home/appuser/src/waterquality/models && \
    chown -R appuser:appuser /home/appuser/src/waterquality/models


USER appuser

RUN python waterquality/pipeline.py

FROM python:3.12-slim AS api

COPY --from=build  /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages
COPY  --from=build /home/appuser/src/waterquality/models /home/appuser/src/waterquality/models
COPY  --from=build /home/appuser/src/waterquality/predict.py /home/appuser/src/waterquality/predict.py
COPY  --from=build /home/appuser/src/app.py /home/appuser/src/app.py

WORKDIR /home/appuser/src

ENV MODEL_PATH='/home/appuser/src/waterquality/models'
ENV MODEL_NAME='waterquality_model.pkl'
ENV HOST='0.0.0.0'
ENV PORT=8000

EXPOSE 8000

CMD ["python","app.py"]
