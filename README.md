# ohtuvarasto

[![GHA workflow badge](https://github.com/villeoikkonen/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/villeoikkonen/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/villeoikkonen/ohtuvarasto/graph/badge.svg?token=DTPK0W9G36)](https://codecov.io/github/villeoikkonen/ohtuvarasto)

## Warehouse web interface

The Flask interface lets you create named warehouses with individual
capacities, view each warehouse's inventory, and add or remove stock. Stock
operations use the existing `Varasto` model. Warehouses are held in memory and
will be cleared when the server stops.

From the repository root, install dependencies and start the development
server with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
uv run python src/app.py
```

Open <http://127.0.0.1:5000> in a browser. Run the tests with:

```sh
uv run coverage run --branch -m pytest
```
