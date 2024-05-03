FROM python:3.12

WORKDIR /app


COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . .
RUN chmod a+x entrypoint/*.sh