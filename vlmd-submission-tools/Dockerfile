FROM quay.io/cdis/python:python3.9-buster-master

RUN pip install --upgrade pip poetry

WORKDIR /opt
COPY poetry.lock /opt/
COPY pyproject.toml /opt/
COPY vlmd_submission_tools/__main__.py /opt/vlmd_submission_tools/__main__.py
RUN python -m venv /env \
    && . /env/bin/activate \
    && poetry install --only main --no-interaction
COPY . /opt/

ENTRYPOINT ["/env/bin/vlmd-submission-tools"]
