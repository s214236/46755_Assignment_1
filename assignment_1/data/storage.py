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
                "capacity": 500,
                "charge_cap": 250,
                "discharge_cap": 250,
                "charge_eff": 0.95,
                "discharge_eff": 0.95,
                "initial_soc": 0.5,
            }
        }
        return self.storage_data
