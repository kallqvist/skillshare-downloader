FROM python:2.7-slim
RUN pip install requests
COPY ./code /code
WORKDIR /code
