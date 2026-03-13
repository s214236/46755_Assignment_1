"""Assignment 1, Step 5: Balancing market."""

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.models.single_period_no_network import SinglePeriodNoNetwork


def main() -> None:
    """Main code for step 5."""
    gen_data = Generation("single_period").generation_data
    demand_data = Demand("single_period").demand_data

    model = SinglePeriodNoNetwork(gen_data, demand_data)
    model.create_model()
    model.optimize()
    model.define_imbalance(
        gen_new_imbalance={
            "G6": 0,
            "G13": gen_data["G13"]["capacity"] * 0.85,
            "G14": gen_data["G14"]["capacity"] * 1.1,
            "G15": gen_data["G15"]["capacity"] * 0.85,
            "G16": gen_data["G16"]["capacity"] * 1.1,
        },
        demand_new_imbalance={},
        gen_regulation={
            gen: {
                "up_reg": gen_data[gen]["capacity"] - model.generation[gen],
                "down_reg": model.generation[gen],
                "cost_up_reg": model.day_ahead_price + gen_data[gen]["cost"] * 0.1,
                "cost_down_reg": model.day_ahead_price - gen_data[gen]["cost"] * 0.15,
            }
            for gen in ["G1", "G2", "G3", "G4"]
        },
        demand_regulation={
            demand: {
                "up_reg": model.demand[demand],
                "down_reg": 0,
                "cost_up_reg": 500,
                "cost_down_reg": 0,
            }
            for demand in demand_data
        },
    )
    model.create_imbalance_model()
    model.optimize_imbalance_model()
    print("RESULTS:")
    print(f"Day-ahead price: {model.day_ahead_price}")
    print(f"Imbalance price: {model.imbalance_price}")

    gen_revenue_day_ahead = {
        gen: model.generation[gen] * model.day_ahead_price for gen in model.gen_data
    }
    gen_revenue_active_imbalance = {
        gen: model.gen_up_reg[gen] * model.imbalance_price
        - model.gen_down_reg[gen] * model.imbalance_price
        for gen in model.gen_data
    }
    gen_revenue_passive_imbalance_twoprice = {
        gen: model.gen_imbalance[gen]["up_reg"]
        * (
            model.day_ahead_price
            if model.imbalance_direction == "downward"
            else model.imbalance_price
        )
        - model.gen_imbalance[gen]["down_reg"]
        * (
            model.day_ahead_price
            if model.imbalance_direction == "upward"
            else model.imbalance_price
        )
        for gen in model.gen_data
    }
    gen_revenue_passive_imbalance_oneprice = {
        gen: model.gen_imbalance[gen]["up_reg"] * model.imbalance_price
        - model.gen_imbalance[gen]["down_reg"] * model.imbalance_price
        for gen in model.gen_data
    }
    gen_cost = {
        gen: (
            model.generation[gen]
            + model.gen_up_reg[gen]
            - model.gen_down_reg[gen]
            + model.gen_imbalance[gen]["up_reg"]
            - model.gen_imbalance[gen]["down_reg"]
        )
        * gen_data[gen]["cost"]
        for gen in model.gen_data
    }

    print("Generation cash flow:")
    for gen in model.gen_data:
        print(
            f"{gen}: Day-ahead revenue: {gen_revenue_day_ahead[gen]:.2f}, "
            f"Active imbalance revenue: {gen_revenue_active_imbalance[gen]:.2f}, "
            f"Passive imbalance revenue (two-price): {gen_revenue_passive_imbalance_twoprice[gen]:.2f}, "
            f"Passive imbalance revenue (one-price): {gen_revenue_passive_imbalance_oneprice[gen]:.2f}, "
            f"Cost: {gen_cost[gen]:.2f}, "
            f"Net cash flow (two-price): {gen_revenue_day_ahead[gen] + gen_revenue_active_imbalance[gen] + gen_revenue_passive_imbalance_twoprice[gen] - gen_cost[gen]:.2f}, "
            f"Net cash flow (one-price): {gen_revenue_day_ahead[gen] + gen_revenue_active_imbalance[gen] + gen_revenue_passive_imbalance_oneprice[gen] - gen_cost[gen]:.2f}"
        )


if __name__ == "__main__":
    main()
