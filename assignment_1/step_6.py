"""Assignment 1, Step 6: Reserve Market."""

from assignment_1.data.demand import Demand
from assignment_1.data.generation import Generation
from assignment_1.models.single_period_no_network import SinglePeriodNoNetwork


def main() -> None:
    """Main code for step 6."""
    gen_data = Generation("single_period").generation_data
    demand_data = Demand("single_period").demand_data

    model = SinglePeriodNoNetwork(gen_data, demand_data)
    total_demand = sum(demand_data[demand]["capacity"] for demand in demand_data)
    model.define_reserve(
        reserve_up_reg=0.15 * total_demand,
        reserve_down_reg=0.1 * total_demand,
        reserve_gens=["G1", "G2", "G3", "G4"],
    )
    model.create_reserve_model()
    model.optimize_reserve_model()
    print("RESERVE RESULTS:")
    print(f"Total reserve cost: {model.total_reserve_cost:.2f}")
    print(f"Reserve price up: {model.reserve_price_up:.2f}")
    print(f"Reserve price down: {model.reserve_price_down:.2f}")
    for gen in model.reserve_gens:
        print(
            f"{gen}: Up reserve: {model.gen_up_reserve[gen]:.2f} MW, "
            f"Down reserve: {model.gen_down_reserve[gen]:.2f} MW"
        )

    model.create_dayahead_model(use_restricitons_from_reserve_model=True)
    model.optimize_dayahead_model()
    print("DAYAHEAD RESULTS:")
    print(f"Day Ahead Market Clearing price: {model.day_ahead_price:.2f}")
    print(f"Social welfare: {model.social_welfare:.2f}")
    print("Generation:")
    for gen, generation in model.generation.items():
        print(f"{gen}: {generation}")
    print("Demand:")
    for demand, demand_value in model.demand.items():
        print(f"{demand}: {demand_value}")


if __name__ == "__main__":
    main()
