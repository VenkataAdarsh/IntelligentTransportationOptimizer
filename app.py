
from flask import Flask, render_template
from database.db_connection import get_db_connection

# Import all route blueprints
from routes.optimizer_routes import optimizer_bp
from routes.vehicle_routes import vehicle_bp
from routes.routes_routes import routes_bp
from routes.report_routes import report_bp

# Create Flask application
app = Flask(__name__)

# Secret key
app.secret_key = "transport_optimizer_secret"

# Register all blueprints
app.register_blueprint(optimizer_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(report_bp)


# Home / Dashboard
@app.route("/")
def dashboard():
    connection = get_db_connection()

    total_vehicles = 0
    total_routes = 0

    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM vehicles")
        total_vehicles = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM routes")
        total_routes = cursor.fetchone()[0]

        cursor.close()
        connection.close()

    return render_template(
        "index.html",
        total_vehicles=total_vehicles,
        total_routes=total_routes
    )


# Display registered URLs
print("REGISTERED URLS:")
print(app.url_map)


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
