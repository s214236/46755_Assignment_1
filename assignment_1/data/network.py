"""Network data."""

from typing import Literal


class NetworkData:
    """Network data."""

    def __init__(self, type: str | Literal["24_bus", "test"]) -> None:
        """Initialize network data."""
        if type == "24_bus":
            self.network_data = self.get_24_bus_network()
        elif type == "test":
            self.network_data = self.get_test_network()
        else:
            raise ValueError("Undefined network data")

    def get_test_network(self) -> dict:
        """Get test network data."""
        self.network_data = {
            "nodes": {
                "1": {"bz": "BZ_1"},
                "2": {"bz": "BZ_2"},
            },
            "lines": {
                "L1": {"from": "1", "to": "2", "reactance": 10, "capacity": 10},
            },
        }

        return self.network_data

    def get_24_bus_network(self) -> dict:
        """Get 24 bus network data."""
        self.network_data = {
            "nodes": {
                "1": {"bz": "TODO: define bz"},
                "2": {"bz": "TODO: define bz"},
                "3": {"bz": "TODO: define bz"},
            },
            "lines": {
                "L1": {"from": "1", "to": "2", "reactance": 10, "capacity": 100},
                "L2": {"from": "1", "to": "3", "reactance": 5, "capacity": 50},
                "L3": {"from": "2", "to": "3", "reactance": 15, "capacity": 150},
            },
        }

        return self.network_data
