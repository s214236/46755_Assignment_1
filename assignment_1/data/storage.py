"""Storage data."""

from typing import Literal


class Storage:
    """Storage data."""

    def __init__(self) -> None:
        """Initialize storage data."""
        self.storage_data = self.get_storage_data()

    def get_storage_data(self) -> dict:
        """Get storage data."""
        self.storage_data = {
            "S1": {
                "type": "storage",
                "node": "TODO: add node",
                "capacity": 200,
                "charge_cap": 100,
                "discharge_cap": 100,
                "charge_eff": 0.9,
                "discharge_eff": 0.9,
                "initial_soc": 1,
            }
        }
        return self.storage_data
