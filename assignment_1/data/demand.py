"""Demand data."""

from typing import Literal

import numpy as np


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
            "demand_1": {"type": "demand", "node": "1", "capacity": 84, "cost": 100},
            "demand_2": {"type": "demand", "node": "2", "capacity": 75, "cost": 100},
            "demand_3": {"type": "demand", "node": "3", "capacity": 139, "cost": 100},
            "demand_4": {"type": "demand", "node": "4", "capacity": 58, "cost": 100},
            "demand_5": {"type": "demand", "node": "5", "capacity": 55, "cost": 100},
            "demand_6": {"type": "demand", "node": "6", "capacity": 106, "cost": 100},
            "demand_7": {"type": "demand", "node": "7", "capacity": 97, "cost": 100},
            "demand_8": {"type": "demand", "node": "8", "capacity": 132, "cost": 100},
            "demand_9": {"type": "demand", "node": "9", "capacity": 135, "cost": 100},
            "demand_10": {"type": "demand", "node": "10", "capacity": 150, "cost": 100},
            "demand_11": {"type": "demand", "node": "13", "capacity": 205, "cost": 100},
            "demand_12": {"type": "demand", "node": "14", "capacity": 150, "cost": 100},
            "demand_13": {"type": "demand", "node": "15", "capacity": 245, "cost": 100},
            "demand_14": {"type": "demand", "node": "16", "capacity": 77, "cost": 100},
            "demand_15": {"type": "demand", "node": "18", "capacity": 258, "cost": 100},
            "demand_16": {"type": "demand", "node": "19", "capacity": 141, "cost": 100},
            "demand_17": {"type": "demand", "node": "20", "capacity": 100, "cost": 100},
        }
        return self.demand_data

    def get_multi_period_demand(self) -> dict:
        """Get multi period demand data."""
        Load_profile = [
            1775.835,
            1669.815,
            1590.3,
            1563.795,
            1563.795,
            1590.3,
            1961.37,
            2279.43,
            2517.975,
            2544.48,
            2544.48,
            2517.975,
            2517.975,
            2517.975,
            2464.965,
            2464.965,
            2623.995,
            2650.5,
            2650.5,
            2544.48,
            2411.955,
            2199.915,
            1934.865,
            1669.815,
        ]

        self.demand_data = {
            "demand_1": {
                "type": "demand",
                "node": "1",
                "capacity": (0.038 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_2": {
                "type": "demand",
                "node": "2",
                "capacity": (0.034 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_3": {
                "type": "demand",
                "node": "3",
                "capacity": (0.063 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_4": {
                "type": "demand",
                "node": "4",
                "capacity": (0.026 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_5": {
                "type": "demand",
                "node": "5",
                "capacity": (0.025 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_6": {
                "type": "demand",
                "node": "6",
                "capacity": (0.048 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_7": {
                "type": "demand",
                "node": "7",
                "capacity": (0.044 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_8": {
                "type": "demand",
                "node": "8",
                "capacity": (0.06 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_9": {
                "type": "demand",
                "node": "9",
                "capacity": (0.061 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_10": {
                "type": "demand",
                "node": "10",
                "capacity": (0.068 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_11": {
                "type": "demand",
                "node": "13",
                "capacity": (0.093 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_12": {
                "type": "demand",
                "node": "14",
                "capacity": (0.068 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_13": {
                "type": "demand",
                "node": "15",
                "capacity": (0.111 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_14": {
                "type": "demand",
                "node": "16",
                "capacity": (0.035 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_15": {
                "type": "demand",
                "node": "18",
                "capacity": (0.117 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_16": {
                "type": "demand",
                "node": "19",
                "capacity": (0.064 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
            "demand_17": {
                "type": "demand",
                "node": "20",
                "capacity": (0.045 * np.array(Load_profile)).tolist(),
                "cost": [100] * 24,
            },
        }
        return self.demand_data


if __name__ == "__main__":
    demand = Demand(type="multi_period")
    print(demand.demand_data)
