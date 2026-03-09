"""Assignment 1, Step 3: Network Constraints."""

import copy

import gurobipy as gp
import matplotlib.pyplot as plt
import numpy as np
from gurobipy import GRB

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.data.network import NetworkData


def optimization_model(
    gen_data: dict,
    demand_data: dict,
    network_data: dict,
    zonal_model: bool = False,
    borders_for_atc_factor: list[str] | None = None,
    atc_factor: float = 1.0,
    create_missing_nodes: bool = False,
) -> tuple[gp.Model, dict, dict]:
    """Optimization model for step 3.

    Args:
        gen_data (dict): Generation data.
        demand_data (dict): Demand data.
        network_data (dict): Network data.
        zonal_model (bool, optional): Whether to analyze the network as combined bidding zones.
            Default is False.
        borders_for_atc_factor (list[str], optional): List of borders to apply the ATC factor to.
            Use the format "<bz_1>_<bz_2>".
            Default is None, which means the ATC factor will be applied to all borders.
        atc_factor (float, optional): Adjust the ATC by a fixed factor.
            Default is 1.0 (no adjustment).
        create_missing_nodes (bool, optional): Whether to create missing nodes in the network data based on generation and demand data.
            Default is False.

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
            if create_missing_nodes:
                network_data["nodes"][node] = {"bz": f"no_bz_node_{node}"}
            else:
                raise ValueError(f"Node {node} is missing in the network data.")

    bzs = list(set(node["bz"] for node in network_data["nodes"].values()))
    atc: dict[str, float] = {}
    for line_data in network_data["lines"].values():
        from_bz = network_data["nodes"][line_data["from"]]["bz"]
        to_bz = network_data["nodes"][line_data["to"]]["bz"]
        if from_bz != to_bz:
            capacity = line_data["capacity"]
            if f"{from_bz}_{to_bz}" not in atc:
                if f"{to_bz}_{from_bz}" not in atc:
                    atc[f"{from_bz}_{to_bz}"] = 0
                    atc[f"{from_bz}_{to_bz}"] += capacity * (
                        atc_factor
                        if borders_for_atc_factor is None
                        or f"{from_bz}_{to_bz}" in borders_for_atc_factor
                        else 1.0
                    )
                else:
                    atc[f"{to_bz}_{from_bz}"] += capacity * (
                        atc_factor
                        if borders_for_atc_factor is None
                        or f"{to_bz}_{from_bz}" in borders_for_atc_factor
                        else 1.0
                    )
            else:
                atc[f"{from_bz}_{to_bz}"] += capacity * (
                    atc_factor
                    if borders_for_atc_factor is None
                    or f"{from_bz}_{to_bz}" in borders_for_atc_factor
                    else 1.0
                )

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

    # Add node voltage angle variables or powerflow variables
    if zonal_model:
        for flow in atc:
            var[f"flow_{flow}"] = model.addVar(lb=-atc[flow], ub=atc[flow])
    else:
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
    if not zonal_model:
        ref_node = list(network_data["nodes"].keys())[0]
        constr["ref_node"] = model.addLConstr(var[f"theta_{ref_node}"] == 0)

    # Add power balance constraint
    if zonal_model:
        for bz in bzs:
            constr[f"power_balance_{bz}"] = model.addLConstr(
                gp.quicksum(
                    var[demand]
                    for demand in demand_data
                    if network_data["nodes"][demand_data[demand]["node"]]["bz"] == bz
                )
                + gp.quicksum(
                    var[f"flow_{flow}"] * (1 if flow.startswith(bz) else -1)
                    for flow in atc
                    if bz in flow
                )
                - gp.quicksum(
                    var[gen]
                    for gen in gen_data
                    if network_data["nodes"][gen_data[gen]["node"]]["bz"] == bz
                )
                == 0,
            )
    else:
        for node in network_data["nodes"]:
            constr[f"power_balance_{node}"] = model.addLConstr(
                gp.quicksum(
                    var[demand]
                    for demand in demand_data
                    if demand_data[demand]["node"] == node
                )
                + gp.quicksum(
                    (
                        var[f"theta_{line_data['from']}"]
                        - var[f"theta_{line_data['to']}"]
                    )
                    / line_data["reactance"]
                    * (1 if line_data["from"] == node else -1)
                    for line_data in network_data["lines"].values()
                    if line_data["from"] == node or line_data["to"] == node
                )
                - gp.quicksum(
                    var[gen] for gen in gen_data if gen_data[gen]["node"] == node
                )
                == 0,
            )

    # Add line flow constraints
    if not zonal_model:
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


def main_1() -> None:
    """Main code for step 3 - Nodal Market Prices.

    A single-period, multi-bidding-zone market clearing model with network constraints.

    """
    # Load data
    gen_data = Generation(type="single_period").generation_data
    demand_data = Demand(type="single_period").demand_data
    network_data = NetworkData(type="24_bus").network_data

    # Run optimization model
    model, var, constr = optimization_model(gen_data, demand_data, network_data)

    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        print(f"Optimal social welfare: {model.ObjVal:.2f} €")
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


def main_2(lines: str | list[str], capacity_factors: list[float] | None = None) -> None:
    """Main code for step 3 - Sensitivity Analysis.

    Analyze nodal prices to changes in line capacities.

    Args:
        lines (str | list[str]): Line name(s) to analyze.
        capacity_factors (list[float], optional): List of capacity factors to apply to the line capacity.
            Default is np.arange(0, 2.1, 0.1).tolist().

    """
    if capacity_factors is None:
        capacity_factors = np.arange(0, 2.1, 0.1).tolist()

    # Load data
    gen_data = Generation(type="single_period").generation_data
    demand_data = Demand(type="single_period").demand_data
    network_data = NetworkData(type="24_bus").network_data

    # Making sure lines is a list
    if isinstance(lines, str):
        lines = [lines]

    # Loop with different line capacities
    nodal_prices: dict[str, list[float]] = {}
    for capacity_factor in capacity_factors:
        # Initialize network data with modified line capacity
        network_data_sensitivity = copy.deepcopy(network_data)
        for line in lines:
            network_data_sensitivity["lines"][line]["capacity"] *= capacity_factor

        # Run optimization model
        model, var, constr = optimization_model(
            gen_data, demand_data, network_data_sensitivity
        )

        # Get nodal prices
        for node in network_data["nodes"]:
            if node not in nodal_prices:
                nodal_prices[node] = []
            nodal_prices[node].append(constr[f"power_balance_{node}"].Pi)

    # Plot nodal prices vs line capacity factor
    plt.figure(figsize=(10, 6))
    for node, prices in nodal_prices.items():
        plt.plot(capacity_factors, prices, label=f"Node {node}")
    plt.xlabel("Line Capacity Factor")
    plt.ylabel("Nodal Price")
    plt.title("Sensitivity Analysis: Nodal Prices vs Line Capacity")
    plt.legend()
    plt.show()


def main_3(
    borders: str | list[str] | None = None, capacity_factors: list[float] | None = None
) -> None:
    """Main code for step 3 - Zonal Market Prices.

    A single-period, multi-bidding-zone market clearing model with ATC constraints.

    Args:
        borders (str | list[str] | None): Which borders to consider the sensitivity analysis.
            Use the format "<bz_1>_<bz_2>".
            Default is None which means all borders are considered.
        capacity_factors (list[float], optional): List of capacity factors to apply to the line capacity.
            Default is None.

    """
    # Load data
    gen_data = Generation(type="single_period").generation_data
    demand_data = Demand(type="single_period").demand_data
    network_data = NetworkData(type="24_bus").network_data

    # Run optimization model
    model, var, constr = optimization_model(
        gen_data, demand_data, network_data, zonal_model=True
    )

    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        print(f"Optimal social welfare: {model.ObjVal:.2f} €")
        market_clearing_prices = {
            bz: constr[f"power_balance_{bz}"].Pi
            for bz in set(node["bz"] for node in network_data["nodes"].values())
        }
        print("Market clearing prices: ", market_clearing_prices)

        for gen in gen_data:
            print(f"Generation {gen}: {var[gen].X} MW")

        for demand in demand_data:
            print(f"Demand {demand}: {var[demand].X} MW")

    else:
        print("No optimal solution found.")

    # Skipping sensitivity analysis if no borders are provided
    if (borders is None) and (capacity_factors is None):
        return

    # Making sure borders is a list
    if isinstance(borders, str):
        borders = [borders]

    if capacity_factors is None:
        capacity_factors = np.arange(0, 2.1, 0.1).tolist()

    # Loop with different ATC capacities
    bz_prices: dict[str, list[float]] = {}
    for capacity_factor in capacity_factors:
        # Run optimization model
        model, var, constr = optimization_model(
            gen_data,
            demand_data,
            network_data,
            zonal_model=True,
            borders_for_atc_factor=borders,
            atc_factor=capacity_factor,
        )

        # Get bz prices
        for bz in set(node["bz"] for node in network_data["nodes"].values()):
            if bz not in bz_prices:
                bz_prices[bz] = []
            bz_prices[bz].append(constr[f"power_balance_{bz}"].Pi)

    # Plot bz prices vs ATC capacity factor
    plt.figure(figsize=(10, 6))
    for bz, prices in bz_prices.items():
        plt.plot(capacity_factors, prices, label=f"Zone {bz}")
    plt.xlabel("ATC Capacity Factor")
    plt.ylabel("Zonal Price")
    plt.title("Sensitivity Analysis: Zonal Prices vs ATC Capacity")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    print("\n\nNodal Market Prices:")
    main_1()

    print("\n\nSensitivity Analysis:")
    main_2(lines=["L1", "L2", "L3"], capacity_factors=np.arange(0, 1.1, 0.01).tolist())

    print("\n\nZonal Market Prices:")
    main_3()
    main_3(borders=["BZ1_BZ2"], capacity_factors=np.arange(0, 1.1, 0.1).tolist())
