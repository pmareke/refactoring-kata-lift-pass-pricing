# Components
This repository is a work in progress exercise applying **Ports and Adapters** to a weather app.

The app exposes an API endpoint included in the **Delivery** layer, this layer talks
with the **Use Cases** layer using command handlers.

These command handlers talks with the **Infrastructure** and **Domain** layers and returns
the result to the **Delivery** layer again.

# App Layers
- Delivery: API using Flask.
- Infrastructure: MariaDB repository.
- Use Cases: Command and Query handlers.
- Domain: Domain objects.

# API endpoints

- GET    - `/prices`: get price for a given lift.
- POST   - `/prices`: get prices for multiple lifts.
- PUT    - `/prices`: add prices in the system.

# How to test it

- `make test`

# How to test with coverage

- `make test-coverage`

# How to format

- `make format`

# How to check for typing

- `make check-typing`
