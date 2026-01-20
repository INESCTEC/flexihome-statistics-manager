# How to run the tests

## Initial setup

### Define secrets

There are TWO main secrets you need to export:
- Influx token
- Gitlab deploy tokens

```bash
# influx db token
export INFLUX_LOCAL_TOKEN=token

# hems-auth
export GITLAB_DEPLOY_USERNAME=...
export GITLAB_DEPLOY_TOKEN=...
# ssa-manager
export GITLAB_SSA_DEPLOY_USERNAME=...
export GITLAB_SSA_MANAGER_DEPLOY_TOKEN=...
```

### Run support containers

Run all containers that support the tests. Defined in Docker-compose/docker-compose.yml:

```bash
# DBs + Kafka
docker compose up postgresql influx-db-service zookeeper kafka connect

# Account manager service
docker compose up account-manager
```

NOTE: You can access influx on **http://localhost:8086** with the credentials define on the docker-compose.yml influx-db-service.<br/>
NOTE: You can access postgresql database with the **psql** command line utility:

```bash
# Use the credentials on docker-compose.yml postgresql service
psql -h 127.0.0.1 -U postgres -d account_manager
```

#### Caveats

The docker-compose.yml file uses the latest production image.
You can change this and re-build the container for the changes to take effect:

```yaml
account-manager:
    image: docker-registry.inesctec.pt/cpes/european-projects/interconnect/hems/hems-services/account-manager-service:staging
    ....
```

```bash
docker compose up --build account-manager
```

### Install tox

```bash
pip install tox
```

## Run tests

There are multiple ways to run the tests:
- All of them
- One test file
- One test class
- One test

```bash
# Run all tests
tox

# Run one test file
tox -e py3 -- statistics_manager_service/test/test_power_queries_controller_consumption_historic.py

# Run one test class
tox -e py3 -- statistics_manager_service/test/test_power_queries_controller_consumption_historic.py::TestPowerQueriesControllerConsumptionHistoric

# Run one test
tox -e py3 -- statistics_manager_service/test/test_power_queries_controller_consumption_historic.py::TestPowerQueriesControllerConsumptionHistoric::test_energy_consumption_get_daily
```

#### Caveats

Tox installs the deps you define on the "tox.ini" file when you run it for the first time and stores it on a ".tox/" folder.

```ini
[testenv]
deps=-r{toxinidir}/test-requirements.txt
     {toxinidir}
```

In our case, **if you change anything on the test-requirements.txt file**, you also need to tell tox to recreate the dependencies using the "-r" flag.

```bash
tox -r ...
```
