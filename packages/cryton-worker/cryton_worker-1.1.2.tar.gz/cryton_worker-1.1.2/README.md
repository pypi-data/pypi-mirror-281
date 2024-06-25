![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-worker/badges/master/coverage.svg)

[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)

# PROJECT HAS BEEN MOVED
The project has been moved to https://gitlab.ics.muni.cz/cryton/cryton. For more information check the [documentation](https://cryton.gitlab-pages.ics.muni.cz/).

# Cryton Worker
Cryton Worker is used for executing attack modules remotely. It utilizes [RabbitMQ](https://www.rabbitmq.com/) 
as its asynchronous remote procedures call protocol. It connects to the Rabbit MQ server and consumes messages from 
the Core component or any other app that implements its RabbitMQ API.

Cryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only 
the latest version is supported** and issues regarding different OS or distributions may **not** be resolved.

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/worker/).

## Quick-start
To be able to execute attack scenarios, you also need to install **[Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core)**.  
Modules provided by Cryton can be found [here](https://gitlab.ics.muni.cz/cryton/cryton-modules). **Their installation will
be covered in this section**.

Make sure Git, Docker, and Docker Compose plugin are installed:
- [Git](https://git-scm.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Optionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).

The following script clones the Worker repository and runs the Docker Compose configuration which starts 
the Worker (with preinstalled modules), and its prerequisites (Metasploit and Empire framework).
```shell
git clone https://gitlab.ics.muni.cz/cryton/cryton-worker.git
cd cryton-worker
docker compose up -d
```

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/worker/).

## Contributing
Contributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-worker)** on gitlab.com.
For more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).
