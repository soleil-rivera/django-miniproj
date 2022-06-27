FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir /workspace
WORKDIR /workspace
# COPY requirements.txt /workspace/
# RUN pip3 install -r requirements.txt
# COPY . /workspace/


COPY pyproject.toml /workspace/
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . /workspace/

CMD [ "python3", "miniproj/manage.py", "runserver", "0.0.0.0:8080"]