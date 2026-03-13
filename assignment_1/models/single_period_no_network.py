"""Single market clearing model, without network constraints."""

import gurobipy as gp
from gurobipy import GRB


class SinglePeriodNoNetwork:
    """Single-period market clearing model without network constraints."""

    def __init__(
        self,
        gen_data: dict[str, dict[str, float]],
        demand_data: dict[str, dict[str, float]],
    ) -> None:
        """Initialize the model."""
        self.gen_data = gen_data
        self.demand_data = demand_data

    def create_model(
        self,
    ) -> None:
        """Single-period market clearing model without network constraints.

        Args:
        gen_data (dict): Generation data.
        demand_data (dict): Demand data.

        """
        # Create a new model
        self.model = gp.Model("single_period_no_network")
        self.var: dict[str, gp.Var] = {}
        self.constr: dict[str, gp.Constr] = {}

        # Add demand variables
        for demand, data in self.demand_data.items():
            self.var[demand] = self.model.addVar(
                lb=0,
                ub=data["capacity"],
            )

        # Add generation variables
        for gen, data in self.gen_data.items():
            self.var[gen] = self.model.addVar(
                lb=0,
                ub=data["capacity"],
            )

        self.model.update()

        # Set objective to maximize social welfare (consumer utility - generation cost)
        self.model.setObjective(
            gp.quicksum(
                data["cost"] * self.var[demand]
                for demand, data in self.demand_data.items()
            )  # Consumer utility
            - gp.quicksum(
                data["cost"] * self.var[gen] for gen, data in self.gen_data.items()
            ),  # Generation cost
            GRB.MAXIMIZE,
        )

        # Add power balance constraint (supply = demand)
        self.constr["power_balance"] = self.model.addLConstr(
            gp.quicksum(self.var[demand] for demand in self.demand_data)
            == gp.quicksum(self.var[gen] for gen in self.gen_data)
        )

    def optimize(self) -> None:
        """Optimize the model, and store the results in the instance."""
        try:
            self.model.optimize()
        except Exception as e:
            print(f"Error occurred while optimizing the model: {e}")

        if self.model.status == GRB.OPTIMAL:
            self.social_welfare = self.model.ObjVal
            self.day_ahead_price = self.constr["power_balance"].Pi
            self.total_generation_cost = sum(
                data["cost"] * self.var[gen].X for gen, data in self.gen_data.items()
            )
            self.total_utility = sum(
                data["cost"] * self.var[demand].X
                for demand, data in self.demand_data.items()
            )
            self.generation = {gen: self.var[gen].X for gen in self.gen_data}
            self.demand = {demand: self.var[demand].X for demand in self.demand_data}

        else:
            print(f"Optimization ended with status {self.model.status}")

    def define_imbalance(
        self,
        gen_new_imbalance: dict[str, float] | None = None,
        demand_new_imbalance: dict[str, float] | None = None,
        gen_regulation: dict[str, dict[str, float]] | None = None,
        demand_regulation: dict[str, dict[str, float]] | None = None,
    ) -> None:
        """Introduce some imbalance at the time of delivery.

        Args:
            gen_new_imbalance (dict[str, float] | None, optional): Generators with new setpoints to introduce imbalance.
                {gen: new_setpoint}, ...}. Defaults to None.
            demand_new_imbalance (dict[str, float] | None, optional): Demands with new setpoints to introduce imbalance.
                {demand: new_setpoint}, ...}. Defaults to None.
            gen_regulation (dict[str, dict[str, float]] | None, optional): Generation regulation capability data.
                {gen: {
                    "max_up_reg": value,
                    "max_down_reg": value,
                    "cost_up_reg": value,
                    "cost_down_reg": value
                    }
                }. Defaults to None.
            demand_regulation (dict[str, dict[str, float]] | None, optional): Demand regulation capability data.
                {demand: {
                    "max_up_reg": value,
                    "max_down_reg": value,
                    "cost_up_reg": value,
                    "cost_down_reg": value
                    }
                }. Defaults to None.

        """
        gen_new_imbalance = gen_new_imbalance or {}
        demand_new_imbalance = demand_new_imbalance or {}
        gen_regulation = gen_regulation or {}
        demand_regulation = demand_regulation or {}

        self.gen_imbalance = {}
        self.demand_imbalance = {}
        for gen in self.generation:
            self.gen_imbalance[gen] = {
                "scheduled": self.generation[gen],
                "up_reg": max(
                    gen_new_imbalance.get(gen, self.generation[gen])
                    - self.generation[gen],
                    0,
                ),
                "down_reg": max(
                    self.generation[gen]
                    - gen_new_imbalance.get(gen, self.generation[gen]),
                    0,
                ),
                "max_up_reg": gen_regulation.get(gen, {}).get("up_reg", 0),
                "max_down_reg": gen_regulation.get(gen, {}).get("down_reg", 0),
                "cost_up_reg": gen_regulation.get(gen, {}).get("cost_up_reg", 0),
                "cost_down_reg": gen_regulation.get(gen, {}).get("cost_down_reg", 0),
            }
        for demand in self.demand:
            self.demand_imbalance[demand] = {
                "scheduled": self.demand[demand],
                "down_reg": max(
                    demand_new_imbalance.get(demand, self.demand[demand])
                    - self.demand[demand],
                    0,
                ),
                "up_reg": max(
                    self.demand[demand]
                    - demand_new_imbalance.get(demand, self.demand[demand]),
                    0,
                ),
                "max_up_reg": demand_regulation.get(demand, {}).get("up_reg", 0),
                "max_down_reg": demand_regulation.get(demand, {}).get("down_reg", 0),
                "cost_up_reg": demand_regulation.get(demand, {}).get("cost_up_reg", 0),
                "cost_down_reg": demand_regulation.get(demand, {}).get(
                    "cost_down_reg", 0
                ),
            }

    def create_imbalance_model(self) -> None:
        """Create a model to clear the imbalance market."""
        self.imbalance_model = gp.Model("imbalance_clearing_model")
        self.imbalance_var: dict[str, gp.Var] = {}
        self.imbalance_constr: dict[str, gp.Constr] = {}

        # Add imbalance variables for generators and demands
        for gen, data in self.gen_imbalance.items():
            self.imbalance_var[f"gen_up_reg_{gen}"] = self.imbalance_model.addVar(
                lb=0,
                ub=data["max_up_reg"],
            )
            self.imbalance_var[f"gen_down_reg_{gen}"] = self.imbalance_model.addVar(
                lb=0,
                ub=data["max_down_reg"],
            )
        for demand, data in self.demand_imbalance.items():
            self.imbalance_var[f"demand_up_reg_{demand}"] = self.imbalance_model.addVar(
                lb=0,
                ub=data["max_up_reg"],
            )
            self.imbalance_var[f"demand_down_reg_{demand}"] = (
                self.imbalance_model.addVar(
                    lb=0,
                    ub=data["max_down_reg"],
                )
            )

        self.imbalance_model.update()

        # Set objective to minimize imbalance cost
        self.imbalance_model.setObjective(
            gp.quicksum(
                data["cost_up_reg"] * self.imbalance_var[f"gen_up_reg_{gen}"]
                - data["cost_down_reg"] * self.imbalance_var[f"gen_down_reg_{gen}"]
                for gen, data in self.gen_imbalance.items()
            )
            + gp.quicksum(
                data["cost_up_reg"] * self.imbalance_var[f"demand_up_reg_{demand}"]
                - data["cost_down_reg"]
                * self.imbalance_var[f"demand_down_reg_{demand}"]
                for demand, data in self.demand_imbalance.items()
            ),
            GRB.MINIMIZE,
        )

        # Add imbalance balance constraint (up_reg - down_reg = imbalance)
        self.imbalance_constr["imbalance_balance"] = self.imbalance_model.addLConstr(
            gp.quicksum(
                self.imbalance_var[f"gen_up_reg_{gen}"]
                - self.imbalance_var[f"gen_down_reg_{gen}"]
                for gen in self.gen_imbalance
            )
            + gp.quicksum(
                self.imbalance_var[f"demand_up_reg_{demand}"]
                - self.imbalance_var[f"demand_down_reg_{demand}"]
                for demand in self.demand_imbalance
            )
            == gp.quicksum(
                data["down_reg"] - data["up_reg"]
                for gen, data in self.gen_imbalance.items()
            )
            + gp.quicksum(
                data["down_reg"] - data["up_reg"]
                for demand, data in self.demand_imbalance.items()
            )
        )

    def optimize_imbalance_model(self) -> None:
        """Optimize the imbalance model, and store the results in the instance."""
        try:
            self.imbalance_model.optimize()
        except Exception as e:
            print(f"Error occurred while optimizing the imbalance model: {e}")

        if self.imbalance_model.status == GRB.OPTIMAL:
            self.total_imbalance_cost = self.imbalance_model.ObjVal
            self.imbalance_price = self.imbalance_constr["imbalance_balance"].Pi
            self.gen_up_reg = {
                gen: self.imbalance_var[f"gen_up_reg_{gen}"].X
                for gen in self.gen_imbalance
            }
            self.gen_down_reg = {
                gen: self.imbalance_var[f"gen_down_reg_{gen}"].X
                for gen in self.gen_imbalance
            }
            self.demand_up_reg = {
                demand: self.imbalance_var[f"demand_up_reg_{demand}"].X
                for demand in self.demand_imbalance
            }
            self.demand_down_reg = {
                demand: self.imbalance_var[f"demand_down_reg_{demand}"].X
                for demand in self.demand_imbalance
            }
            self.imbalance_direction = (
                "downward"
                if sum(
                    self.imbalance_var[f"gen_up_reg_{gen}"].X
                    for gen in self.gen_imbalance
                )
                > sum(
                    self.imbalance_var[f"gen_down_reg_{gen}"].X
                    for gen in self.gen_imbalance
                )
                else "upward"
            )

        else:
            print(
                f"Imbalance optimization ended with status {self.imbalance_model.status}"
            )
