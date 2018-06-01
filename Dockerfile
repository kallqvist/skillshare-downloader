FROM python:2.7-slim
RUN pip install requests
COPY ./code /code
WORKDIR /code
RUN chmod +x from-arguments.py
ENTRYPOINT ["python", "/code/from-arguments.py"]
