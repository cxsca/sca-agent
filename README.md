<p align="center">
  <img width="250px" src="/sca-agent.svg?raw=true">
</p>

The **SCA Agent** is an hybrid on-premise solution for Checkmarx SCA. The agent resolves packages and acts as a proxy to SCA cloud.

> **Disclaimer**
>
> Please note that this is a beta version of the SCA Agent. The product is still under development and testing, and is provided "as-is".

Further documentation can be found in [Checkmarx Knowledge Center](https://checkmarx.atlassian.net/wiki/spaces/CD/pages/2509278941/CxSCA+Agent+BETA).

## Setup

1. Install the latest versions of [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).
2. Download and unzip the release, and run the setup script
    ```shell
    wget https://github.com/cxsca/sca-agent/releases/latest/download/sca-agent.zip
    unzip sca-agent.zip
    sh setup.sh
    ```
3. Configure the `.env` file according to your needs. The `EXTERNAL_HOST` variable must match the DNS or the IP of the machine where the agent is installed.
4. Start the agent:
    ```shell
    docker-compose up -d
    ```
5. You can now verify the agent health from your browser by accessing `http://sca-agent-host/api/health`, or by running a scan using one of [Checkmarx plugins](https://www.checkmarx.com/plugins/).
### Windows

It is recommended to use [WSL2](https://docs.docker.com/docker-for-windows/wsl/) as your docker backend. This way the docker containers are running natively on Linux, and you can use the `setup.sh` script mentioned above.

If you're **not** using WSL2, you can run the `setup.sh` script using docker -
```batch
docker run --rm -it -v //var/run/docker.sock:/var/run/docker.sock -v %cd%:/sca-agent -w /sca-agent docker/compose ./setup.sh
docker-compose up -d
```

## Monitoring

The log files are written in the logs directory by default. The location can be changed by editing `.env`.

## Management

You can start, stop or restart the agent with docker-compose.

```shell
docker-compose down && docker-compose up -d
```
