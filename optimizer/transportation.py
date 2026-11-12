
from scipy.optimize import linprog


def balance_transportation(costs, supply, demand):
    """
    Automatically balance an unbalanced transportation problem.
    """

    if not costs or not supply or not demand:
        raise ValueError("Enter cost, supply and demand values.")

    if len(costs) != len(supply):
        raise ValueError("Cost matrix rows must match supply values.")

    if any(len(row) != len(demand) for row in costs):
        raise ValueError("Cost matrix columns must match demand values.")

    if any(value < 0 for value in supply + demand):
        raise ValueError("Supply and demand cannot be negative.")

    if any(value < 0 for row in costs for value in row):
        raise ValueError("Transportation costs cannot be negative.")

    costs = [list(map(float, row)) for row in costs]
    supply = list(map(float, supply))
    demand = list(map(float, demand))

    source_labels = [
        f"Source {i + 1}" for i in range(len(supply))
    ]

    destination_labels = [
        f"Destination {j + 1}" for j in range(len(demand))
    ]

    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply > total_demand:

        difference = total_supply - total_demand

        # Add a dummy destination with zero cost
        for row in costs:
            row.append(0.0)

        demand.append(difference)
        destination_labels.append("Dummy Destination")

    elif total_demand > total_supply:

        difference = total_demand - total_supply

        # Add a dummy source with zero cost
        dummy_row = [0.0] * len(demand)

        costs.append(dummy_row)
        supply.append(difference)
        source_labels.append("Dummy Source")

    return costs, supply, demand, source_labels, destination_labels


def optimize_transportation(costs, supply, demand):

    # Automatically balance supply and demand
    costs, supply, demand, source_labels, destination_labels = (
        balance_transportation(costs, supply, demand)
    )

    number_of_sources = len(supply)
    number_of_destinations = len(demand)

    # Convert cost matrix into a single list
    cost_list = [
        costs[i][j]
        for i in range(number_of_sources)
        for j in range(number_of_destinations)
    ]

    A_eq = []
    b_eq = []

    # Supply constraints
    for i in range(number_of_sources):

        row = [0] * (number_of_sources * number_of_destinations)

        for j in range(number_of_destinations):
            row[i * number_of_destinations + j] = 1

        A_eq.append(row)
        b_eq.append(supply[i])

    # Demand constraints
    for j in range(number_of_destinations):

        row = [0] * (number_of_sources * number_of_destinations)

        for i in range(number_of_sources):
            row[i * number_of_destinations + j] = 1

        A_eq.append(row)
        b_eq.append(demand[j])

    # Solve using Linear Programming
    result = linprog(
        cost_list,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(0, None),
        method="highs"
    )

    if not result.success:
        raise ValueError("Optimization failed: " + result.message)

    # Convert solution into allocation matrix
    allocation = []

    for i in range(number_of_sources):

        row = []

        for j in range(number_of_destinations):

            value = result.x[
                i * number_of_destinations + j
            ]

            row.append(round(float(value), 2))

        allocation.append(row)

    minimum_cost = round(float(result.fun), 2)

    return allocation, minimum_cost
