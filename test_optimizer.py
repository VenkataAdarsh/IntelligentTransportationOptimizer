
from optimizer.transportation import optimize_transportation

costs = [
    [4, 6, 8],
    [5, 3, 7],
    [6, 5, 4]
]

supply = [100, 150, 120]

demand = [120, 130, 120]

allocation, minimum_cost = optimize_transportation(
    costs, supply, demand
)

print("Optimal Allocation:")

for row in allocation:
    print(row)

print("Minimum Transportation Cost:", minimum_cost)
