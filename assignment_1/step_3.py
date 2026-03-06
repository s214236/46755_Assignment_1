"""Assignment 1, Step 3: Network Constraints."""

import gurobipy as gp
import matplotlib.pyplot as plt
from gurobipy import GRB

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.data.network import NetworkData


def optimization_model(
    gen_data: dict, demand_data: dict, network_data: dict
) -> tuple[gp.Model, dict, dict]:
    """Optimization model for step 3.

    Args:
        gen_data (dict): Generation data.
        demand_data (dict): Demand data.
        network_data (dict): Network data.

    Returns:
        model (gp.Model): Gurobi optimization model.
        var (dict): Dictionary of variables.
        constr (dict): Dictionary of constraints.

    """
    # Create a new model
    model = gp.Model("step_3")
    var = {}
    constr = {}

    # Adding missing nodes in the network data
    nodes = [gen["node"] for gen in gen_data.values()] + [
        demand["node"] for demand in demand_data.values()
    ]
    for node in nodes:
        if node not in network_data["nodes"]:
            network_data["nodes"][node] = {"bz": f"no_bz_node_{node}"}

    # Add demand variables
    for demand, data in demand_data.items():
        var[demand] = model.addVar(
            lb=0,
            ub=data["capacity"],
        )

    # Add generation variables
    for gen, data in gen_data.items():
        var[gen] = model.addVar(
            lb=0,
            ub=data["capacity"],
        )

    # Add node voltage angle variables
    for node in network_data["nodes"]:
        var[f"theta_{node}"] = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY)

    model.update()

    # Set objective to maximize social welfare (consumer utility - generation cost)
    model.setObjective(
        gp.quicksum(
            data["cost"] * var[demand] for demand, data in demand_data.items()
        )  # Consumer utility
        - gp.quicksum(
            data["cost"] * var[gen] for gen, data in gen_data.items()
        ),  # Generation cost
        GRB.MAXIMIZE,
    )

    # Add reference bus constraint (set voltage angle of one node to 0)
    ref_node = list(network_data["nodes"].keys())[0]
    constr["ref_node"] = model.addLConstr(var[f"theta_{ref_node}"] == 0)

    # Add power balance constraint
    for node in network_data["nodes"]:
        constr[f"power_balance_{node}"] = model.addLConstr(
            gp.quicksum(
                var[demand]
                for demand in demand_data
                if demand_data[demand]["node"] == node
            )
            + gp.quicksum(
                (var[f"theta_{line_data['from']}"] - var[f"theta_{line_data['to']}"])
                / line_data["reactance"]
                * (1 if line_data["from"] == node else -1)
                for line_data in network_data["lines"].values()
                if line_data["from"] == node or line_data["to"] == node
            )
            - gp.quicksum(var[gen] for gen in gen_data if gen_data[gen]["node"] == node)
            == 0,
        )

    # Add line flow constraints
    for line_name, line_data in network_data["lines"].items():
        constr[f"line_flow_{line_name}_pos"] = model.addLConstr(
            (var[f"theta_{line_data['from']}"] - var[f"theta_{line_data['to']}"])
            / line_data["reactance"]
            <= line_data["capacity"]
        )
        constr[f"line_flow_{line_name}_neg"] = model.addLConstr(
            (var[f"theta_{line_data['from']}"] - var[f"theta_{line_data['to']}"])
            / line_data["reactance"]
            >= -line_data["capacity"]
        )
    # Optimize model
    model.optimize()

    return model, var, constr


def main(plot: bool = True) -> None:
    """Main code for step 3.

    A single-period, multi-bidding-zone market clearing model with network constraints.

    Args:
        plot (bool, optional): Whether to plot. Defaults to True.

    """
    # %% Load data
    gen_data = Generation(type="single_period").generation_data
    demand_data = Demand(type="single_period").demand_data
    network_data = NetworkData(type="24_bus").network_data

    model, var, constr = optimization_model(gen_data, demand_data, network_data)

    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        market_clearing_prices = {
            node: constr[f"power_balance_{node}"].Pi for node in network_data["nodes"]
        }
        print("Market clearing prices: ", market_clearing_prices)

        for gen in gen_data:
            print(f"Generation {gen}: {var[gen].X} MW")

        for demand in demand_data:
            print(f"Demand {demand}: {var[demand].X} MW")

        print("Line flows:")
        for line_name, line_data in network_data["lines"].items():
            flow = (
                var[f"theta_{line_data['from']}"].X - var[f"theta_{line_data['to']}"].X
            ) / line_data["reactance"]
            print(
                f"  {line_name}: {line_data['from']} -> {line_data['to']} : {flow} MW"
            )

    else:
        print("No optimal solution found.")


if __name__ == "__main__":
    main()
    print("Done!")
