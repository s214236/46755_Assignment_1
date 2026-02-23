"""Assignment 1, Step 1: Copper-Plate, Single Hour."""

import gurobipy as gp
import matplotlib.pyplot as plt
from gurobipy import GRB

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.utils.colors import demand_color, gen_color


def main(plot: bool = True) -> None:
    """Main code for step 1.

    A single-period, single-bidding-zone (copper-plate) market clearing model.

    Args:
        plot (bool, optional): Whether to plot. Defaults to True.

    """
    # %% Load data
    gen_data = Generation(type="single_period").generation_data
    demand_data = Demand(type="single_period").demand_data

    # %% Optimization model
    # Create a new model
    model = gp.Model("step_1")
    var = {}
    constr = {}

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

    # Add power balance constraint (supply = demand)
    constr["power_balance"] = model.addLConstr(
        gp.quicksum(var[demand] for demand in demand_data)
        == gp.quicksum(var[gen] for gen in gen_data),
    )

    # Optimize model
    model.optimize()

    # %% Evaluate results
    if model.status == GRB.OPTIMAL:
        print("\nRESULTS:")
        spot_price = constr["power_balance"].Pi
        print(f"Market clearing price: {spot_price:.2f} €/MWh")
        print(f"Optimal social welfare: {model.ObjVal:.2f} €")
        total_cost = sum(data["cost"] * var[gen].X for gen, data in gen_data.items())
        print(f"Total generation cost: {total_cost:.2f} €")

        print("Generation:")
        for gen, data in gen_data.items():
            profit = (spot_price - data["cost"]) * var[gen].X
            print(f"  {gen}: {var[gen].X:.2f} MW --- Total profit: {profit:.2f} €")

        print("Demand:")
        for demand, data in demand_data.items():
            utility = (data["cost"] - spot_price) * var[demand].X
            print(
                f"  {demand}: {var[demand].X:.2f} MW --- Total utility: {utility:.2f} €"
            )

        # %% Plot supply and demand curves
        if plot:
            plt.figure(figsize=(10, 6))
            # Sorted for merit order
            sorted_gen = sorted(gen_data.items(), key=lambda item: item[1]["cost"])
            sorted_demand = sorted(
                demand_data.items(), key=lambda item: item[1]["cost"], reverse=True
            )

            # Plot supply curve
            supply_x = [0]
            supply_y = [sorted_gen[0][1]["cost"]]
            prev_x = 0
            for name, data in sorted_gen:
                current_x = prev_x + data["capacity"]

                supply_x.append(current_x)
                supply_y.append(data["cost"])

                # Add label
                mid_x = prev_x + data["capacity"] / 2
                mid_y = data["cost"]
                plt.text(
                    mid_x,
                    mid_y + 0.5,
                    name,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                )

                prev_x = current_x

            plt.step(
                supply_x,
                supply_y,
                where="pre",
                label="Supply Curve",
                color=gen_color,
            )
            plt.scatter(supply_x[1:], supply_y[1:], color=gen_color, zorder=5, s=10)

            # Plot demand curve
            demand_x = [0]
            demand_y = [sorted_demand[0][1]["cost"]]
            prev_x = 0
            for name, data in sorted_demand:
                current_x = prev_x + data["capacity"]

                demand_x.append(current_x)
                demand_y.append(data["cost"])

                # Add label
                mid_x = prev_x + data["capacity"] / 2
                mid_y = data["cost"]
                plt.text(
                    mid_x,
                    mid_y + 0.5,
                    name,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                )
                prev_x = current_x

            plt.step(
                demand_x,
                demand_y,
                where="pre",
                label="Demand Curve",
                color=demand_color,
            )
            plt.scatter(demand_x[1:], demand_y[1:], color=demand_color, zorder=5, s=10)

            # Show spot price
            plt.axhline(
                spot_price,
                color="black",
                linestyle="--",
                label="Market Clearing Price",
                alpha=0.5,
            )

            plt.xlabel("Capacity (MW)")
            plt.ylabel("Price (€/MWh)")
            plt.title("Supply and Demand Curves")
            plt.legend()
            plt.grid()
            plt.show()

    else:
        print("No optimal solution found.")


if __name__ == "__main__":
    main(plot=True)
