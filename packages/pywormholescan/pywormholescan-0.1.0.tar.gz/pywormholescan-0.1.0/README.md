# PyWormholescan
PyWormholescan is a Python wrapper that simplifies interaction with the [Wormholescan API](https://api.wormholescan.io). It allows developers to leverage the power of Wormholescan's data and functionality using pure Python syntax.

## Installation
```sh
pip install pywormholescan
```

## Usage
1. Import the WormholescanAPI class.
    ```python
    from pywormholescan import WormholescanAPI, Network
    ```

2. Create an instance of WormholescanAPI
    ```python
    w = WormholescanAPI(network=Network.MAINNET)
    ```

3. Explore the available methods:

    Refer to the [official Wormholescan API documentation](https://api.wormholescan.io) for a comprehensive list of available methods and their parameters.

## Note

URL path variables are required arguments and can be passed either as positional or keyword arguments. However, URL query variables must be passed as keyword arguments.
This module allows developers to use standard Python syntax. Non-required query variables, such as `pageSize` from the core API, can be written in snake case (`page_size`). However, required query variables, such as `time_span`, must be written with snake case.

## Examples
```pycon
# Check health status.
>>> w.get_health_check()
{'status': 'OK'}

# Get token by chain and address.
# In this example, notice how path variables can be passed as positional arguments.
>>> token_info = w.get_token_by_chain_and_address(1, "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ")
>>> print(token_info)
{'symbol': 'W', 'coingeckoId': 'wormhole', 'decimals': 6}

>>> print(token_info["symbol"]) # Access token symbol from response
'W'

# Alternatively, pass path variables as keyword arguments.
>>> w.get_token_by_chain_and_address(chain_id=1, token_address="HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3")
{'symbol': 'PYTH', 'coingeckoId': 'pyth-network', 'decimals': 6}


# Get top assets by volume.
# Required query variables like the example below, must be passed as is (in snake case).
>>> w.get_top_assets_by_volume(time_span="7d")
{'assets': [{'emitterChain': 2, 'symbol': 'USDC', 'tokenChain': 2, 'tokenAddress': '000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'volume': '50816690.58171399'}, ...]} # Remainder of output snipped for brevity.
```

## Naming Conventions:
PyWormholescan follows Python snake_case conventions for both method names and arguments, ensuring consistency and readability.

## Documentation
For detailed method descriptions, parameters, and example usage, refer to the [official Wormholescan API documentation](https://api.wormholescan.io).

## Contribution Guidelines

We welcome contributions from the community! If you have bug fixes, improvements, or new features for PyWormholescan, we encourage you to get involved.

Here's a quick guide to contributing:

1. Fork the repository: Create a fork of the PyWormholescan repository on GitHub.
2. Clone your fork: Clone your forked repository to your local machine.
3. Create a new branch: Create a new branch for your contribution.
4. Make changes: Implement your changes and write clear code with docstrings.
5. Test your changes: Thoroughly test your changes to ensure they don't introduce regressions.
6. Commit your changes: Commit your changes with a descriptive commit message.
7. Push your changes: Push your changes to your forked repository on GitHub.
8. Create a pull request: Create a pull request from your branch to the main branch of the upstream PyWormholescan repository.

Additional Tips:
1. Adhere to code style: Follow the existing code style and formatting conventions for consistency.
2. Write clear documentation: If you're adding new features, provide clear documentation within the code using docstrings.
3. Communicate effectively: Clearly explain your changes and reasoning in the pull request description.
4. Review process: We will review your pull request and provide feedback.

We appreciate your contributions to PyWormholescan ❤!
