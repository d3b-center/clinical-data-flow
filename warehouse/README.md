# ⛳️ Playground Clinical Data Flow Warehouse

Temporary data warehouse for development purposes. This will later go away
in favor of the D3b Data Warehouse.

## Quickstart

The warehouse and Metabase are deployed in the Kids First AWS Dev environment.
You must tunnel into this environment in order to access the endpoints.

### Setup Tunnel to Dev Env
Create a tunnel to the dev environment so that you can access the db:

```shell
$ ./dev-env-tunnel.sh dev
```
Get [dev-env-tunnel.sh](https://github.com/kids-first/aws-infra-toolbox/blob/master/scripts/developer_scripts/dev-env-tunnel)

### Endpoints

- **Warehouse DB:** http://10.10.1.191:5431
- **Metabase App:** http://10.10.1.191:3000

## Spin Up Docker Stack

If you want to work locally, spin up a Docker container on your machine

```bash
git clone git@github.com:d3b-center/clinical-data-flow.git
cd clinical-data-flow/warehouse

# Rename smilecdr/dev.env to smilecdr/.env so docker-compose
# can pick up the environment variables at runtime
mv dev.env .env

docker-compose up -d
```

Then use any db client to connect to `localhost:5431` using the db credentials
in `.env`.
