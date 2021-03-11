FROM openjdk:slim

# Install Wget
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean;

# Install Python
RUN apt-get update && \
    apt-get install -y -f python3 && \
    apt-get clean;

COPY scripts ./scripts/
WORKDIR scripts

RUN mkdir CLI

RUN wget -P CLI https://download.checkmarx.com/9.3.0GA/Plugins/CxConsolePlugin-2021.1.3.zip

RUN python3 -m zipfile -e CLI/CxConsolePlugin-2021.1.3.zip CLI
RUN chmod +x CLI/runCxConsole.sh

CMD ["python3", "-W", "ignore" , "test_runner.py"]