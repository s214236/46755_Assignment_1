"""Generation data."""

from typing import Literal


class Generation:
    """Generation data."""

    def __init__(self, type: str | Literal["single_period", "multi_period"]) -> None:
        """Initialize generation data.

        Args:
            type ("single period" | "multi period"): Type of generation data to generate.

        """
        self.type = type
        if self.type == "single_period":
            self.generation_data = self.get_single_period_generation()
        else:
            self.generation_data = self.get_multi_period_generation()

    def get_single_period_generation(self) -> dict:
        """Get single period generation data."""
        self.generation_data = {
            "G1": {"type": "conv", "node": "1", "capacity": 106.4, "cost": 13.32},
            "G2": {"type": "conv", "node": "2", "capacity": 106.4, "cost": 13.32},
            "G3": {"type": "conv", "node": "7", "capacity": 245, "cost": 20.7},
            "G4": {"type": "conv", "node": "13", "capacity": 413.7, "cost": 20.93},
            "G5": {"type": "conv", "node": "15", "capacity": 42, "cost": 26.11},
            "G6": {"type": "conv", "node": "15", "capacity": 108.5, "cost": 10.52},
            "G7": {"type": "conv", "node": "16", "capacity": 108.5, "cost": 10.52},
            "G8": {"type": "conv", "node": "18", "capacity": 280, "cost": 6.02},
            "G9": {"type": "conv", "node": "21", "capacity": 280, "cost": 5.47},
            "G10": {"type": "conv", "node": "22", "capacity": 210, "cost": 7},
            "G11": {"type": "conv", "node": "23", "capacity": 72, "cost": 10.52},
            "G12": {"type": "conv", "node": "23", "capacity": 245, "cost": 10.89},
            "G13": {"type": "wind", "node": "3", "capacity": 120.54, "cost": 0},
            "G14": {"type": "wind", "node": "5", "capacity": 115.52, "cost": 0},
            "G15": {"type": "wind", "node": "16", "capacity": 53.34, "cost": 0},
            "G16": {"type": "wind", "node": "21", "capacity": 38.16, "cost": 0},
        }
        return self.generation_data

    def get_multi_period_generation(self) -> dict:
        """Get multi period generation data.

        Source: Renewables.ninja.
            jan. 1st. 2019
            G13: Ringkøbing, Denmark.
            G14: København, Denmark.
            G15: Berlin, Germany.
            G16: Paris, France.

        """
        self.generation_data = {
            "G1": {
                "type": "conv",
                "node": "1",
                "capacity": [106.4] * 24,
                "cost": [13.32] * 24,
            },
            "G2": {
                "type": "conv",
                "node": "2",
                "capacity": [106.4] * 24,
                "cost": [13.32] * 24,
            },
            "G3": {
                "type": "conv",
                "node": "7",
                "capacity": [245] * 24,
                "cost": [20.7] * 24,
            },
            "G4": {
                "type": "conv",
                "node": "13",
                "capacity": [413.7] * 24,
                "cost": [20.93] * 24,
            },
            "G5": {
                "type": "conv",
                "node": "15",
                "capacity": [42] * 24,
                "cost": [26.11] * 24,
            },
            "G6": {
                "type": "conv",
                "node": "15",
                "capacity": [108.5] * 24,
                "cost": [10.52] * 24,
            },
            "G7": {
                "type": "conv",
                "node": "16",
                "capacity": [108.5] * 24,
                "cost": [10.52] * 24,
            },
            "G8": {
                "type": "conv",
                "node": "18",
                "capacity": [280] * 24,
                "cost": [6.02] * 24,
            },
            "G9": {
                "type": "conv",
                "node": "21",
                "capacity": [280] * 24,
                "cost": [5.47] * 24,
            },
            "G10": {
                "type": "conv",
                "node": "22",
                "capacity": [210] * 24,
                "cost": [7] * 24,
            },
            "G11": {
                "type": "conv",
                "node": "23",
                "capacity": [72] * 24,
                "cost": [10.52] * 24,
            },
            "G12": {
                "type": "conv",
                "node": "23",
                "capacity": [245] * 24,
                "cost": [10.89] * 24,
            },
            "G13": {
                "type": "wind",
                "node": "3",
                "capacity": [
                    493.889,
                    494.944,
                    495.592,
                    494.255,
                    487.672,
                    471.115,
                    461.533,
                    450.362,
                    442.578,
                    434.578,
                    420.067,
                    411.262,
                    408.750,
                    396.238,
                    380.322,
                    359.388,
                    384.210,
                    432.453,
                    465.333,
                    482.747,
                    487.239,
                    489.023,
                    492.153,
                    494.535,
                ],
                "cost": [0] * 24,
            },
            "G14": {
                "type": "wind",
                "node": "5",
                "capacity": [
                    480.869,
                    487.427,
                    492.159,
                    495.046,
                    495.499,
                    495.655,
                    495.415,
                    494.244,
                    490.584,
                    484.157,
                    472.434,
                    456.822,
                    457.264,
                    469.746,
                    484.197,
                    492.592,
                    495.512,
                    495.313,
                    494.575,
                    495.495,
                    495.510,
                    494.879,
                    494.249,
                    493.486,
                ],
                "cost": [0] * 24,
            },
            "G15": {
                "type": "wind",
                "node": "16",
                "capacity": [
                    134.532,
                    174.108,
                    197.026,
                    210.252,
                    228.114,
                    237.570,
                    243.530,
                    249.353,
                    254.906,
                    247.705,
                    242.458,
                    251.672,
                    255.555,
                    257.117,
                    255.880,
                    258.542,
                    262.337,
                    266.566,
                    269.523,
                    270.718,
                    270.139,
                    268.821,
                    266.440,
                    266.848,
                ],
                "cost": [0] * 24,
            },
            "G16": {
                "type": "wind",
                "node": "21",
                "capacity": [
                    31.099,
                    27.833,
                    27.644,
                    31.590,
                    35.887,
                    40.126,
                    41.208,
                    44.025,
                    45.845,
                    41.002,
                    42.247,
                    52.750,
                    56.039,
                    53.706,
                    49.371,
                    55.737,
                    67.571,
                    75.297,
                    80.724,
                    86.684,
                    94.832,
                    106.509,
                    115.965,
                    110.077,
                ],
                "cost": [0] * 24,
            },
        }
        return self.generation_data


if __name__ == "__main__":
    generation = Generation(type="multi_period")
    print(generation.generation_data)
