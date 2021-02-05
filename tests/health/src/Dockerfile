FROM python:slim

WORKDIR scripts

COPY scripts/* .

RUN python3 -m pip install requests

CMD ["python3", "-u", "run_tests.py"]

#CMD tail -f /dev/null