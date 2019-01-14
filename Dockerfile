FROM python:3-slim
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./code /code
WORKDIR /code
# ENTRYPOINT ["python", "/code/from-arguments.py"]
