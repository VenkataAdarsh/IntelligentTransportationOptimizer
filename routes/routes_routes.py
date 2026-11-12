
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db_connection import get_db_connection

routes_bp = Blueprint("transport_routes", __name__)


# Display all routes
@routes_bp.route("/routes")
def show_routes():

    connection = get_db_connection()
    route_list = []

    if connection:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM routes
            ORDER BY route_id DESC
        """)

        route_list = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template("routes.html", routes=route_list)


# Add new route
@routes_bp.route("/add_route", methods=["POST"])
def add_route():

    source = request.form.get("source", "").strip()
    destination = request.form.get("destination", "").strip()

    try:
        distance = float(request.form.get("distance", ""))
        toll_cost = float(request.form.get("toll_cost", "0"))
        fuel_cost = float(request.form.get("fuel_cost", "0"))

        if not source or not destination:
            raise ValueError("Source and destination are required.")

        if distance <= 0 or toll_cost < 0 or fuel_cost < 0:
            raise ValueError("Enter valid distance and costs.")

        connection = get_db_connection()

        if connection is None:
            raise Exception("Database connection failed.")

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO routes
            (source, destination, distance, toll_cost, fuel_cost)
            VALUES (%s, %s, %s, %s, %s)
        """, (source, destination, distance, toll_cost, fuel_cost))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Route added successfully!", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception as error:
        flash("Error adding route: " + str(error), "error")

    return redirect(url_for("transport_routes.show_routes"))


# Edit existing route
@routes_bp.route("/edit_route/<int:route_id>", methods=["POST"])
def edit_route(route_id):

    source = request.form.get("source", "").strip()
    destination = request.form.get("destination", "").strip()

    try:
        distance = float(request.form.get("distance", ""))
        toll_cost = float(request.form.get("toll_cost", "0"))
        fuel_cost = float(request.form.get("fuel_cost", "0"))

        if not source or not destination:
            raise ValueError("Source and destination are required.")

        if distance <= 0 or toll_cost < 0 or fuel_cost < 0:
            raise ValueError("Enter valid distance and costs.")

        connection = get_db_connection()

        if connection is None:
            raise Exception("Database connection failed.")

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE routes
            SET source = %s,
                destination = %s,
                distance = %s,
                toll_cost = %s,
                fuel_cost = %s
            WHERE route_id = %s
        """, (
            source,
            destination,
            distance,
            toll_cost,
            fuel_cost,
            route_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Route updated successfully!", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception as error:
        flash("Error updating route: " + str(error), "error")

    return redirect(url_for("transport_routes.show_routes"))


# Delete route
@routes_bp.route("/delete_route/<int:route_id>", methods=["POST"])
def delete_route(route_id):

    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM routes
            WHERE route_id = %s
        """, (route_id,))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Route deleted successfully!", "success")

    else:
        flash("Database connection failed.", "error")

    return redirect(url_for("transport_routes.show_routes"))
