"""Assignment 1, Step 2: Copper-Plate, Multiple Hours."""

import gurobipy as gp
import matplotlib.pyplot as plt
from gurobipy import GRB

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.data.storage import Storage
from assignment_1.utils.colors import demand_color, gen_color


def main(plot: bool = True) -> None:
    """Main code for step 2.

    A multi-period, single-bidding-zone (copper-plate) market clearing model.

    Args:
        plot (bool, optional): Whether to plot. Defaults to True.

    """
    # %% Load data
    gen_data = Generation(type="multi_period").generation_data
    demand_data = Demand(type="multi_period").demand_data
    storage_data = Storage().storage_data
    T = 24

    # Checking if input data has correct time series length
    for demand, data in demand_data.items():
        assert len(data["capacity"]) == T, (
            f"Demand {demand} has incorrect time series length."
        )
        assert len(data["cost"]) == T, (
            f"Demand {demand} has incorrect time series length."
        )
    for gen, data in gen_data.items():
        assert len(data["capacity"]) == T, (
            f"Generation {gen} has incorrect time series length."
        )
        assert len(data["cost"]) == T, (
            f"Generation {gen} has incorrect time series length."
        )

    # %% Optimization model
    # Create a new model
    model = gp.Model("step_2")
    var = {}
    constr = {}

    # Add variables
    for t in range(T):
        # Add demand variables for each time period
        for demand, data in demand_data.items():
            var[f"{demand}_{t}"] = model.addVar(
                lb=0,
                ub=data["capacity"][t],
            )

        # Add generation variables
        for gen, data in gen_data.items():
            var[f"{gen}_{t}"] = model.addVar(
                lb=0,
                ub=data["capacity"][t],
            )

        # Add Charge/Discharge variables for storage unit
        var[f"charge_{t}"] = model.addVar(
            lb=0,
            ub=storage_data["S1"]["charge_cap"],
        )
        var[f"discharge_{t}"] = model.addVar(
            lb=0,
            ub=storage_data["S1"]["discharge_cap"],
        )

        # Add state of charge variable for storage unit
        var[f"soc_{t}"] = model.addVar(
            lb=0,
            ub=storage_data["S1"]["capacity"],
        )

    model.update()

    # Set objective to maximize social welfare (consumer utility - generation cost)
    model.setObjective(
        gp.quicksum(
            gp.quicksum(
                data["cost"][t] * var[f"{demand}_{t}"]
                for demand, data in demand_data.items()
            )
            for t in range(T)
        )  # Consumer utility
        - gp.quicksum(
            gp.quicksum(
                data["cost"][t] * var[f"{gen}_{t}"] for gen, data in gen_data.items()
            )
            for t in range(T)
        ),  # Generation cost
        GRB.MAXIMIZE,
    )

    # Add constraints
    for t in range(T):
        # Add power balance constraint (supply = demand)
        constr[f"power_balance_{t}"] = model.addLConstr(
            gp.quicksum(var[f"{demand}_{t}"] for demand in demand_data)
            + var[f"charge_{t}"]
            == gp.quicksum(var[f"{gen}_{t}"] for gen in gen_data)
            + var[f"discharge_{t}"],
        )

        # Add storage state of charge constraints
        if t == 0:
            constr[f"soc_balance_{t}"] = model.addLConstr(
                var[f"soc_{t}"]
                == storage_data["S1"]["initial_soc"] * storage_data["S1"]["capacity"]
                + storage_data["S1"]["charge_eff"] * var[f"charge_{t}"]
                - (1 / storage_data["S1"]["discharge_eff"]) * var[f"discharge_{t}"],
            )
        else:
            constr[f"soc_balance_{t}"] = model.addLConstr(
                var[f"soc_{t}"]
                == var[f"soc_{t - 1}"]
                + storage_data["S1"]["charge_eff"] * var[f"charge_{t}"]
                - (1 / storage_data["S1"]["discharge_eff"]) * var[f"discharge_{t}"],
            )

    # Optimize model
    model.optimize()

    # %% Evaluate results
    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        spot_price = [round(constr[f"power_balance_{t}"].Pi, 2) for t in range(T)]
        print(f"Market clearing price: {spot_price} €/MWh")
        print(f"Optimal social welfare: {model.ObjVal:.2f} €")

    else:
        print("No optimal solution found.")


if __name__ == "__main__":
    main(plot=True)
