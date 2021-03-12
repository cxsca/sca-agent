FROM python:slim

COPY scripts ./scripts/

WORKDIR scripts

RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

CMD ["python", "-W", "ignore" , "test_runner.py"]