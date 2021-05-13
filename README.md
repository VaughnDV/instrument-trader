Instrument Trader
====================

A REST API with endpoints serving Trade data from a mocked database.

### Prerequisites

* [Docker](https://docs.docker.com/install/)
* [Docker-Compose](https://docs.docker.com/compose/)

### Local Setup

`docker-compose build`

`docker-compose run instrument-trader pytest`

`docker-compose up`

If all works well, you should be able to view the docs and interact with the API

`http://0.0.0.0:5000/docs`

To generate random test data for manual testing

`http://0.0.0.0:5000/generate_10_random_trades/`

