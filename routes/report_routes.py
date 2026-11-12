
from flask import Blueprint, render_template
from database.db_connection import get_db_connection

report_bp = Blueprint("reports", __name__)


# --------------------------------
# OPTIMIZATION HISTORY
# --------------------------------

@report_bp.route("/history")
def optimization_history():

    history = []
    error = None

    connection = get_db_connection()

    if connection is None:
        error = "Database connection failed."
        return render_template(
            "history.html",
            history=history,
            error=error
        )

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                optimization_id,
                total_cost,
                total_quantity,
                created_at
            FROM optimization_history
            ORDER BY optimization_id DESC
        """)

        history = cursor.fetchall()

        # Get allocation details for every optimization
        for item in history:

            cursor.execute("""
                SELECT
                    source,
                    destination,
                    allocated_quantity,
                    unit_cost,
                    total_cost
                FROM transportation_results
                WHERE optimization_id = %s
                ORDER BY result_id
            """, (item["optimization_id"],))

            item["allocations"] = cursor.fetchall()

    except Exception as e:
        error = str(e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return render_template(
        "history.html",
        history=history,
        error=error
    )


# --------------------------------
# REPORTS DASHBOARD
# --------------------------------

@report_bp.route("/reports")
def reports():

    total_vehicles = 0
    total_routes = 0
    total_optimizations = 0
    total_cost = 0
    average_cost = 0

    history = []
    chart_labels = []
    chart_costs = []
    chart_quantities = []

    connection = get_db_connection()

    if connection:

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM vehicles
            """)
            total_vehicles = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM routes
            """)
            total_routes = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_optimizations,
                    COALESCE(SUM(total_cost), 0) AS total_cost,
                    COALESCE(AVG(total_cost), 0) AS average_cost
                FROM optimization_history
            """)

            stats = cursor.fetchone()

            total_optimizations = stats["total_optimizations"]
            total_cost = float(stats["total_cost"])
            average_cost = float(stats["average_cost"])

            cursor.execute("""
                SELECT
                    optimization_id,
                    total_cost,
                    total_quantity,
                    created_at
                FROM optimization_history
                ORDER BY optimization_id DESC
                LIMIT 10
            """)

            history = cursor.fetchall()

            chart_history = list(reversed(history))

            for item in chart_history:

                chart_labels.append(
                    "Optimization " + str(item["optimization_id"])
                )

                chart_costs.append(float(item["total_cost"]))

                chart_quantities.append(
                    int(item["total_quantity"])
                )

        finally:
            cursor.close()
            connection.close()

    return render_template(
        "reports.html",
        total_vehicles=total_vehicles,
        total_routes=total_routes,
        total_optimizations=total_optimizations,
        total_cost=total_cost,
        average_cost=average_cost,
        history=history,
        chart_labels=chart_labels,
        chart_costs=chart_costs,
        chart_quantities=chart_quantities
    )
