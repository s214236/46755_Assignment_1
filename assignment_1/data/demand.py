"""Demand data."""

from typing import Literal


class Demand:
    """Demand data."""

    def __init__(self, type: str | Literal["single_period", "multi_period"]) -> None:
        """Initialize demand data.

        Args:
            type ("single period" | "multi period"): Type of demand data to generate.

        """
        self.type = type
        if self.type == "single_period":
            self.demand_data = self.get_single_period_demand()
        else:
            self.demand_data = self.get_multi_period_demand()

    def get_single_period_demand(self) -> dict:
        """Get single period demand data."""
        self.demand_data = {
            "demand_1": {"type": "demand", "node": "1", "capacity": 100, "cost": 100},
            "demand_2": {"type": "demand", "node": "2", "capacity": 100, "cost": 100},
            "demand_3": {"type": "demand", "node": "3", "capacity": 100, "cost": 100},
        }
        return self.demand_data

    def get_multi_period_demand(self) -> dict:
        """Get multi period demand data."""
        self.demand_data = {
            "demand_1": {
                "type": "demand",
                "node": "1",
                "capacity": [100] * 24,
                "cost": [100] * 24,
            },
            "demand_2": {
                "type": "demand",
                "node": "2",
                "capacity": [100] * 24,
                "cost": [100] * 24,
            },
            "demand_3": {
                "type": "demand",
                "node": "3",
                "capacity": [100] * 24,
                "cost": [100] * 24,
            },
        }
        return self.demand_data


if __name__ == "__main__":
    demand = Demand(type="single_period")
    print(demand.demand_data)
