"""Network data."""


class NetworkData:
    """Network data."""

    def __init__(self) -> None:
        """Initialize network data."""
        self.network_data = self.get_24_bus_network()

    def get_24_bus_network(self) -> dict:
        """Get 24 bus network data."""
        self.network_data = {
            "nodes": {
                "1": {"bz": "BZ1"},
                "2": {"bz": "BZ1"},
                "3": {"bz": "BZ1"},
                "4": {"bz": "BZ1"},
                "5": {"bz": "BZ1"},
                "6": {"bz": "BZ1"},
                "7": {"bz": "BZ1"},
                "8": {"bz": "BZ1"},
                "9": {"bz": "BZ1"},
                "10": {"bz": "BZ1"},
                "11": {"bz": "BZ1"},
                "12": {"bz": "BZ1"},
                "13": {"bz": "BZ1"},
                "14": {"bz": "BZ2"},
                "15": {"bz": "BZ2"},
                "16": {"bz": "BZ2"},
                "17": {"bz": "BZ2"},
                "18": {"bz": "BZ2"},
                "19": {"bz": "BZ2"},
                "20": {"bz": "BZ2"},
                "21": {"bz": "BZ2"},
                "22": {"bz": "BZ2"},
                "23": {"bz": "BZ2"},
                "24": {"bz": "BZ2"},
            },
            "lines": {
                "L1": {"from": "1", "to": "2", "reactance": 0.0147, "capacity": 175},
                "L2": {"from": "1", "to": "3", "reactance": 0.2253, "capacity": 175},
                "L3": {"from": "1", "to": "5", "reactance": 0.0907, "capacity": 350},
                "L4": {"from": "2", "to": "4", "reactance": 0.1356, "capacity": 175},
                "L5": {"from": "2", "to": "6", "reactance": 0.205, "capacity": 175},
                "L6": {"from": "3", "to": "9", "reactance": 0.1271, "capacity": 175},
                "L7": {"from": "3", "to": "24", "reactance": 0.084, "capacity": 400},
                "L8": {"from": "4", "to": "9", "reactance": 0.111, "capacity": 175},
                "L9": {"from": "5", "to": "10", "reactance": 0.094, "capacity": 350},
                "L10": {"from": "6", "to": "10", "reactance": 0.0642, "capacity": 175},
                "L11": {"from": "7", "to": "8", "reactance": 0.0652, "capacity": 350},
                "L12": {"from": "8", "to": "9", "reactance": 0.1762, "capacity": 175},
                "L13": {"from": "8", "to": "10", "reactance": 0.1762, "capacity": 175},
                "L14": {"from": "9", "to": "11", "reactance": 0.084, "capacity": 400},
                "L15": {"from": "9", "to": "12", "reactance": 0.084, "capacity": 400},
                "L16": {"from": "10", "to": "11", "reactance": 0.084, "capacity": 400},
                "L17": {"from": "10", "to": "12", "reactance": 0.084, "capacity": 400},
                "L18": {"from": "11", "to": "13", "reactance": 0.0488, "capacity": 500},
                "L19": {"from": "11", "to": "14", "reactance": 0.0426, "capacity": 500},
                "L20": {"from": "12", "to": "13", "reactance": 0.0488, "capacity": 500},
                "L21": {"from": "12", "to": "23", "reactance": 0.0985, "capacity": 500},
                "L22": {"from": "13", "to": "23", "reactance": 0.0884, "capacity": 500},
                "L23": {"from": "14", "to": "16", "reactance": 0.0594, "capacity": 500},
                "L24": {"from": "15", "to": "16", "reactance": 0.0172, "capacity": 500},
                "L25": {
                    "from": "15",
                    "to": "21",
                    "reactance": 0.0249,
                    "capacity": 1000,
                },
                "L26": {"from": "15", "to": "24", "reactance": 0.0529, "capacity": 500},
                "L27": {"from": "16", "to": "17", "reactance": 0.0263, "capacity": 500},
                "L28": {"from": "16", "to": "19", "reactance": 0.0234, "capacity": 500},
                "L29": {"from": "17", "to": "18", "reactance": 0.0143, "capacity": 500},
                "L30": {"from": "17", "to": "22", "reactance": 0.1069, "capacity": 500},
                "L31": {
                    "from": "18",
                    "to": "21",
                    "reactance": 0.0132,
                    "capacity": 1000,
                },
                "L32": {
                    "from": "19",
                    "to": "20",
                    "reactance": 0.0203,
                    "capacity": 1000,
                },
                "L33": {
                    "from": "20",
                    "to": "23",
                    "reactance": 0.0112,
                    "capacity": 1000,
                },
                "L34": {"from": "21", "to": "22", "reactance": 0.0692, "capacity": 500},
            },
        }

        return self.network_data
