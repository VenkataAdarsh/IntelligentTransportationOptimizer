
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db_connection import get_db_connection

vehicle_bp = Blueprint("vehicles", __name__)


# Display all vehicles
@vehicle_bp.route("/vehicles")
def vehicles():

    connection = get_db_connection()
    vehicle_list = []

    if connection:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM vehicles ORDER BY vehicle_id DESC")
        vehicle_list = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template("vehicles.html", vehicles=vehicle_list)


# Add vehicle
@vehicle_bp.route("/add_vehicle", methods=["POST"])
def add_vehicle():

    name = request.form.get("vehicle_name", "").strip()
    vehicle_type = request.form.get("vehicle_type", "").strip()
    capacity = request.form.get("capacity", "").strip()
    fuel_cost = request.form.get("fuel_cost", "").strip()
    status = request.form.get("status", "Available")

    try:
        if not name or not vehicle_type:
            raise ValueError()

        capacity = int(capacity)
        fuel_cost = float(fuel_cost)

        if capacity <= 0 or fuel_cost < 0:
            raise ValueError()

        connection = get_db_connection()

        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO vehicles
                (vehicle_name, vehicle_type, capacity, fuel_cost, status)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (name, vehicle_type, capacity, fuel_cost, status)
            )

            connection.commit()
            cursor.close()
            connection.close()

            flash("Vehicle added successfully!", "success")
        else:
            flash("Database connection failed.", "error")

    except ValueError:
        flash("Please enter valid vehicle details.", "error")

    return redirect(url_for("vehicles.vehicles"))


# Edit vehicle
@vehicle_bp.route("/edit_vehicle/<int:vehicle_id>", methods=["POST"])
def edit_vehicle(vehicle_id):

    name = request.form.get("vehicle_name", "").strip()
    vehicle_type = request.form.get("vehicle_type", "").strip()
    capacity = request.form.get("capacity", "").strip()
    fuel_cost = request.form.get("fuel_cost", "").strip()
    status = request.form.get("status", "Available")

    try:
        if not name or not vehicle_type:
            raise ValueError()

        capacity = int(capacity)
        fuel_cost = float(fuel_cost)

        if capacity <= 0 or fuel_cost < 0:
            raise ValueError()

        connection = get_db_connection()

        if connection:
            cursor = connection.cursor()

            query = """
                UPDATE vehicles
                SET vehicle_name=%s,
                    vehicle_type=%s,
                    capacity=%s,
                    fuel_cost=%s,
                    status=%s
                WHERE vehicle_id=%s
            """

            cursor.execute(
                query,
                (name, vehicle_type, capacity, fuel_cost, status, vehicle_id)
            )

            connection.commit()
            cursor.close()
            connection.close()

            flash("Vehicle updated successfully!", "success")
        else:
            flash("Database connection failed.", "error")

    except ValueError:
        flash("Please enter valid vehicle details.", "error")

    return redirect(url_for("vehicles.vehicles"))


# Delete vehicle
@vehicle_bp.route("/delete_vehicle/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):

    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM vehicles WHERE vehicle_id = %s",
            (vehicle_id,)
        )

        connection.commit()
        cursor.close()
        connection.close()

        flash("Vehicle deleted successfully!", "success")
    else:
        flash("Database connection failed.", "error")

    return redirect(url_for("vehicles.vehicles"))
