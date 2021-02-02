Simple HTTP server returning calendar entries for all [Wekan](https://github.com/wekan/wekan) cards with set due date. To be used with Lightning or similar calendar app (read-only).
Yes, it's not the best solution, but it does the job (at least for me).
Depends on: https://github.com/wekan/wekan-python-api-client.

This is a fork of https://github.com/LukasGasior1/wekan-ical-server.git. It updates the server to Python 3 and adds a Dockerfile and docker-compose.yml to run it as a Docker container.

Configuration:
Edit the docker-compose.yml file environment section for configuration:

* `WEKAN_HOST`: Hostname of your wekan server
* `WEKAN_USER`: Wekan username
* `WEKAN_PASSWORD`: Wekan password
* `LISTEN_HOST`: Hostname of the ical server (default: 0.0.0.0)
* `LISTEN_PORT`: Port of the ical server (default: 8091)

Running:
Start the server with the following command:

```bash
$ docker-compose up
```

