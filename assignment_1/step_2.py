"""Assignment 1, Step 2: Copper-Plate, Multiple Hours."""

import copy

import gurobipy as gp
import matplotlib.pyplot as plt
import numpy as np
from gurobipy import GRB

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.data.storage import Storage
from assignment_1.utils.colors import demand_color, gen_color


def optimization_model(
    gen_data: dict,
    demand_data: dict,
    storage_data: dict,
    T: int,
) -> tuple[gp.Model, dict, dict]:
    """Create optimization model for step 2.

    Args:
        gen_data (dict): Generation data.
        demand_data (dict): Demand data.
        storage_data (dict): Storage data.
        T (int): Number of time periods.

    Returns:
        model (gp.Model): Gurobi optimization model.
        var (dict): Dictionary of optimization variables.
        constr (dict): Dictionary of optimization constraints.

    """
    # Checking if input data has correct time series length
    for demand, data in demand_data.items():
        if len(data["capacity"]) != T:
            raise ValueError(
                f"Demand {demand} has incorrect time series length."
            )
        if len(data["cost"]) != T:
            raise ValueError(
                f"Demand {demand} has incorrect time series length."
            )
    for gen, data in gen_data.items():
        if len(data["capacity"]) != T:
            raise ValueError(
                f"Generation {gen} has incorrect time series length."
            )
        if len(data["cost"]) != T:
            raise ValueError(
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
        for storage, data in storage_data.items():
            var[f"{storage}_charge_{t}"] = model.addVar(
                lb=0,
                ub=data["charge_cap"],
            )
            var[f"{storage}_discharge_{t}"] = model.addVar(
                lb=0,
                ub=data["discharge_cap"],
            )

            # Add state of charge variable for storage unit
            var[f"{storage}_soc_{t}"] = model.addVar(
                lb=0,
                ub=data["capacity"],
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
            + gp.quicksum(var[f"{storage}_charge_{t}"] for storage in storage_data)
            == gp.quicksum(var[f"{gen}_{t}"] for gen in gen_data)
            + gp.quicksum(var[f"{storage}_discharge_{t}"] for storage in storage_data),
        )

        # Add storage state of charge constraints
        for storage in storage_data:
            constr[f"soc_balance_{storage}_{t}"] = model.addLConstr(
                var[f"{storage}_soc_{t}"]
                == (
                    var[f"{storage}_soc_{t - 1}"]
                    if t > 0
                    else storage_data[storage]["initial_soc"]
                    * storage_data[storage]["capacity"]
                )
                + storage_data[storage]["charge_eff"] * var[f"{storage}_charge_{t}"]
                - (1 / storage_data[storage]["discharge_eff"])
                * var[f"{storage}_discharge_{t}"],
            )

    # Optimize model
    model.optimize()

    return model, var, constr

def print_merit_order(
        gen_data: dict,
        var: dict,
        spot_price: list,
        T: int) -> None:
    """Print merit order and marginal generator for each hour."""
    print("\nMERIT ORDER BY HOUR")

    for t in range(T):
        print(f"\nHour {t} | Market price: {spot_price[t]} €/MWh")

        # Collect generator info
        generators = []
        for gen, data in gen_data.items():
            output = var[f"{gen}_{t}"].X
            capacity = data["capacity"][t]
            cost = data["cost"][t]

            generators.append((gen, cost, output, capacity))

        # Sort by offer price (merit order)
        generators.sort(key=lambda x: x[1])

        # Print merit order
        for gen, cost, output, capacity in generators:
            status = ""

            if output > 1e-5 and output < capacity - 1e-5:
                status = " <-- MARGINAL"
            elif output >= capacity - 1e-5:
                status = " (at capacity)"

            print(
                f"{gen:15s} | offer: {cost:6.2f} €/MWh | "
                f"dispatch: {output:6.2f}/{capacity:6.2f} MW{status}"
            )



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

    # %% Optimization model
    model, var, constr = optimization_model(gen_data, demand_data, storage_data, T)
    
    model_without_storage, _, constr_without_storage = optimization_model(
    gen_data, demand_data, {}, T
    )

    # %% Evaluate results
    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        spot_price = [round(constr[f"power_balance_{t}"].Pi, 2) for t in range(T)]
        print(f"Market clearing price: {spot_price} €/MWh")
        print_merit_order(gen_data, var, spot_price, T)
        print(f"Optimal social welfare: {model.ObjVal:.2f} €")
        total_cost = sum(
            data["cost"][t] * var[f"{gen}_{t}"].X
            for gen, data in gen_data.items()
            for t in range(T)
        )
        print(f"Total generation cost: {total_cost:.2f} €")

        print("Generation:")
        for gen, data in gen_data.items():
            profit = sum(
                (spot_price[t] - data["cost"][t]) * var[f"{gen}_{t}"].X
                for t in range(T)
            )
            print(f"  {gen} total profit: {profit:.2f} €")

        print("Demand:")
        for demand, data in demand_data.items():
            utility = sum(
                (data["cost"][t] - spot_price[t]) * var[f"{demand}_{t}"].X
                for t in range(T)
            )
            print(f"  {demand}: total utility: {utility:.2f} €")

        print("Storage:")
        for storage in storage_data:
            profit = sum(
                spot_price[t]
                * (var[f"{storage}_discharge_{t}"].X - var[f"{storage}_charge_{t}"].X)
                for t in range(T)
            )
            print(f"  {storage} total profit: {profit:.2f} €")

        spot_price_without_storage = [
            round(constr_without_storage[f"power_balance_{t}"].Pi, 2) for t in range(T)
        ]


        if plot:
            plt.figure(figsize=(10, 6))
            plt.step(
                range(T + 1),
                spot_price + [spot_price[-1]],
                where="post",
                label="Market Clearing Price",
                color="black",
            )
            plt.step(
                range(T + 1),
                spot_price_without_storage + [spot_price_without_storage[-1]],
                where="post",
                label="Market Clearing Price (without storage)",
                color="red",
            )
            plt.xlabel("Time (hours)")
            plt.xticks(np.arange(0, T + 1, 3))
            plt.ylabel("Price (€/MWh)")
            plt.title("Market Clearing Price")
            plt.legend()
            plt.grid(True)
            plt.show()

    else:
        print("No optimal solution found.")
        return

    # %% Sensitivity analysis on storage parameters
    def storage_param_sensitivity_analysis(
        storage_data: dict, factors: list[float], param: str
    ) -> list[tuple[float, float]]:
        social_welfare_results = []
        for factor in factors:
            # Update storage data with sensitivity factor
            storage_data_sensitivity = copy.deepcopy(storage_data)
            for storage in storage_data_sensitivity:
                match param:
                    case "capacity":
                        storage_data_sensitivity[storage]["capacity"] *= factor
                    case "power":
                        storage_data_sensitivity[storage]["charge_cap"] *= factor
                        storage_data_sensitivity[storage]["discharge_cap"] *= factor
                    case _:
                        raise ValueError("Invalid parameter for sensitivity analysis.")

            model_sensitivity, _, _ = optimization_model(
                gen_data, demand_data, storage_data_sensitivity, T
            )

            if model_sensitivity.status == GRB.OPTIMAL:
                social_welfare_results.append((factor, model_sensitivity.ObjVal))
            else:
                raise ValueError(
                    f"No optimal solution found for sensitivity factor {factor} for parameter {param}."
                )

        return social_welfare_results

    if plot:
        factors = np.arange(0.5, 1.6, 0.1).tolist()
        results_capacity = storage_param_sensitivity_analysis(
            storage_data, factors, "capacity"
        )
        results_charge_cap = storage_param_sensitivity_analysis(
            storage_data, factors, "power"
        )

        plt.figure(figsize=(10, 6))
        plt.plot(
            [factor for factor, _ in results_capacity],
            [welfare for _, welfare in results_capacity],
            label="Storage Capacity",
            marker="o",
        )
        plt.plot(
            [factor for factor, _ in results_charge_cap],
            [welfare for _, welfare in results_charge_cap],
            label="Storage Power",
            marker="s",
        )
        plt.xlabel("Sensitivity Factor")
        plt.ylabel("Social Welfare (€)")
        plt.title("Sensitivity Analysis of Storage Parameters")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main(plot=True)


# %% Merit order





