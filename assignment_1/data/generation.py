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
            "gen_1": {"type": "conv", "node": "1", "capacity": 100, "cost": 100},
            "gen_2": {"type": "wind", "node": "2", "capacity": 100, "cost": 0},
            "gen_3": {"type": "solar", "node": "3", "capacity": 100, "cost": 0},
        }
        return self.generation_data

    def get_multi_period_generation(self) -> dict:
        """Get multi period generation data."""
        self.generation_data = {
            "gen_1": {
                "type": "conv",
                "node": "1",
                "capacity": [100] * 24,
                "cost": [100] * 24,
            },
            "gen_2": {
                "type": "wind",
                "node": "2",
                "capacity": [100] * 24,
                "cost": [0] * 24,
            },
            "gen_3": {
                "type": "solar",
                "node": "3",
                "capacity": [100] * 24,
                "cost": [0] * 24,
            },
        }
        return self.generation_data


if __name__ == "__main__":
    generation = Generation(type="single_period")
    print(generation.generation_data)
