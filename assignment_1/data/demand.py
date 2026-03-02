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
            "D1": {"type": "demand", "node": "1", "capacity": 84, "cost": 30},
            "D2": {"type": "demand", "node": "2", "capacity": 75, "cost": 28},
            "D3": {"type": "demand", "node": "3", "capacity": 139, "cost": 26},
            "D4": {"type": "demand", "node": "4", "capacity": 58, "cost": 24},
            "D5": {"type": "demand", "node": "5", "capacity": 55, "cost": 23},
            "D6": {"type": "demand", "node": "6", "capacity": 106, "cost": 22},
            "D7": {"type": "demand", "node": "7", "capacity": 97, "cost": 21},
            "D8": {"type": "demand", "node": "8", "capacity": 132, "cost": 20},
            "D9": {"type": "demand", "node": "9", "capacity": 135, "cost": 19},
            "D10": {"type": "demand", "node": "10", "capacity": 150, "cost": 18},
            "D11": {"type": "demand", "node": "13", "capacity": 205, "cost": 17},
            "D12": {"type": "demand", "node": "14", "capacity": 150, "cost": 16},
            "D13": {"type": "demand", "node": "15", "capacity": 245, "cost": 15},
            "D14": {"type": "demand", "node": "16", "capacity": 77, "cost": 14},
            "D15": {"type": "demand", "node": "18", "capacity": 258, "cost": 13},
            "D16": {"type": "demand", "node": "19", "capacity": 141, "cost": 12},
            "D17": {"type": "demand", "node": "20", "capacity": 100, "cost": 11},
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
        bid_max = 1.5
        bid_min = 0.5
        bid_profile = [1.0] * len(Load_profile)
        for i in range(len(bid_profile)):
            bid_profile[i] = bid_min + (bid_max - bid_min) * (
                Load_profile[i] - min(Load_profile)
            ) / (max(Load_profile) - min(Load_profile))

        single_period_demand = self.get_single_period_demand()

        self.demand_data = {
            "D1": {
                "type": "demand",
                "node": "1",
                "capacity": (0.038 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D1"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D2": {
                "type": "demand",
                "node": "2",
                "capacity": (0.034 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D2"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D3": {
                "type": "demand",
                "node": "3",
                "capacity": (0.063 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D3"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D4": {
                "type": "demand",
                "node": "4",
                "capacity": (0.026 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D4"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D5": {
                "type": "demand",
                "node": "5",
                "capacity": (0.025 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D5"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D6": {
                "type": "demand",
                "node": "6",
                "capacity": (0.048 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D6"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D7": {
                "type": "demand",
                "node": "7",
                "capacity": (0.044 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D7"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D8": {
                "type": "demand",
                "node": "8",
                "capacity": (0.06 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D8"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D9": {
                "type": "demand",
                "node": "9",
                "capacity": (0.061 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D9"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D10": {
                "type": "demand",
                "node": "10",
                "capacity": (0.068 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D10"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D11": {
                "type": "demand",
                "node": "13",
                "capacity": (0.093 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D11"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D12": {
                "type": "demand",
                "node": "14",
                "capacity": (0.068 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D12"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D13": {
                "type": "demand",
                "node": "15",
                "capacity": (0.111 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D13"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D14": {
                "type": "demand",
                "node": "16",
                "capacity": (0.035 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D14"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D15": {
                "type": "demand",
                "node": "18",
                "capacity": (0.117 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D15"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D16": {
                "type": "demand",
                "node": "19",
                "capacity": (0.064 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D16"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
            "D17": {
                "type": "demand",
                "node": "20",
                "capacity": (0.045 * np.array(Load_profile)).tolist(),
                "cost": [
                    bid_profile[i] * single_period_demand["D17"]["cost"]
                    for i in range(len(bid_profile))
                ],
            },
        }
        return self.demand_data


if __name__ == "__main__":
    demand = Demand(type="multi_period")
    print(demand.demand_data["D10"])
