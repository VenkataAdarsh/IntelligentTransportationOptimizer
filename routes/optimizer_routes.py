
from flask import Blueprint, render_template, request, flash
from database.db_connection import get_db_connection
from optimizer.transportation import (
    optimize_transportation,
    balance_transportation
)

optimizer_bp = Blueprint("optimizer", __name__)


@optimizer_bp.route("/optimizer", methods=["GET", "POST"])
def optimizer():

    result = None
    error = None

    if request.method == "POST":

        connection = None
        cursor = None

        try:
            # Read transportation cost matrix
            cost_text = request.form.get("costs", "").strip()

            costs = [
                [float(value.strip()) for value in line.split(",")]
                for line in cost_text.splitlines()
                if line.strip()
            ]

            # Read supply
            supply = [
                float(value.strip())
                for value in request.form.get("supply", "").split(",")
                if value.strip()
            ]

            # Read demand
            demand = [
                float(value.strip())
                for value in request.form.get("demand", "").split(",")
                if value.strip()
            ]

            if not costs or not supply or not demand:
                raise ValueError("Please enter all values.")

            # Check that quantities are whole numbers
            if any(value != int(value) for value in supply + demand):
                raise ValueError("Supply and demand must be whole numbers.")

            # Balance the transportation problem
            (
                balanced_costs,
                balanced_supply,
                balanced_demand,
                source_labels,
                destination_labels
            ) = balance_transportation(costs, supply, demand)

            # Calculate optimal allocation
            allocation, minimum_cost = optimize_transportation(
                costs, supply, demand
            )

            total_quantity = int(sum(balanced_supply))

            # Connect to MySQL
            connection = get_db_connection()

            if connection is None:
                raise Exception("MySQL database connection failed.")

            cursor = connection.cursor()

            # Save optimization history
            cursor.execute("""
                INSERT INTO optimization_history
                (total_cost, total_quantity)
                VALUES (%s, %s)
            """, (minimum_cost, total_quantity))

            optimization_id = cursor.lastrowid

            # Save transportation allocation
            for i, row in enumerate(allocation):

                for j, quantity in enumerate(row):

                    if quantity > 0:

                        unit_cost = balanced_costs[i][j]
                        total_cost = quantity * unit_cost

                        cursor.execute("""
                            INSERT INTO transportation_results
                            (
                                optimization_id,
                                source,
                                destination,
                                allocated_quantity,
                                unit_cost,
                                total_cost
                            )
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            optimization_id,
                            source_labels[i],
                            destination_labels[j],
                            int(round(quantity)),
                            unit_cost,
                            total_cost
                        ))

            connection.commit()

            result = {
                "allocation": allocation,
                "minimum_cost": minimum_cost,
                "optimization_id": optimization_id,
                "source_labels": source_labels,
                "destination_labels": destination_labels,
                "original_supply": supply,
                "original_demand": demand,
                "balanced_supply": balanced_supply,
                "balanced_demand": balanced_demand
            }

            flash("Optimization completed and saved successfully!", "success")

        except Exception as e:

            if connection:
                connection.rollback()

            error = str(e)

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template(
        "optimizer.html",
        result=result,
        error=error
    )
