from typing import Any

import aiohttp
import requests

from .network import Network


class APIClient:
    def __init__(self, network: Network) -> None:
        if not isinstance(network, Network):
            raise ValueError(
                "Invalid network provided. Please use Network.MAINNET or Network.TESTNET."
            )

        self.base_url = network.value
        self.timeout = 120

    def get(self, endpoint: str) -> dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GET request failed: {e}")
            raise

    def post(self, endpoint: str, json: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=json, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"POST request failed: {e}")
            raise
