"""Flask user interface for the warehouse application."""

from dataclasses import dataclass
import math

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from varasto import Varasto


@dataclass
class Warehouse:
    """A named warehouse backed by the existing inventory model."""

    id: int
    name: str
    inventory: Varasto


def create_app(test_config=None):
    """Create and configure the web application."""
    # Route registration naturally groups the app's small set of handlers.
    # pylint: disable=too-many-statements
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(SECRET_KEY="warehouse-development-key")
    if test_config:
        flask_app.config.update(test_config)

    flask_app.extensions["warehouses"] = []
    flask_app.extensions["next_warehouse_id"] = 1

    @flask_app.template_filter("number")
    def number_filter(value):
        return format_number(value)

    def find_warehouse(warehouse_id):
        for warehouse in flask_app.extensions["warehouses"]:
            if warehouse.id == warehouse_id:
                return warehouse
        abort(404)

    @flask_app.get("/")
    def index():
        warehouses = flask_app.extensions["warehouses"]
        return render_template("index.html", warehouses=warehouses)

    @flask_app.post("/warehouses")
    # Keep validation and creation together as one form action.
    # pylint: disable=too-many-statements
    def create_warehouse():
        name = request.form.get("name", "").strip()
        capacity = parse_positive_number(request.form.get("capacity"))
        if not name:
            flash("Enter a name for the warehouse.", "error")
        elif any(warehouse.name.casefold() == name.casefold()
                 for warehouse in flask_app.extensions["warehouses"]):
            flash("A warehouse with that name already exists.", "error")
        elif capacity is None:
            flash("Capacity must be a number greater than zero.", "error")
        else:
            warehouse_id = flask_app.extensions["next_warehouse_id"]
            flask_app.extensions["next_warehouse_id"] = warehouse_id + 1
            flask_app.extensions["warehouses"].append(
                Warehouse(warehouse_id, name, Varasto(capacity))
            )
            flash(f"Warehouse {name} created.", "success")
        return redirect(url_for("index"))

    @flask_app.post("/warehouses/<int:warehouse_id>/add")
    def add_stock(warehouse_id):
        warehouse = find_warehouse(warehouse_id)
        quantity = parse_positive_number(request.form.get("quantity"))
        if quantity is None:
            flash("Quantity must be a number greater than zero.", "error")
        else:
            before = warehouse.inventory.saldo
            warehouse.inventory.lisaa_varastoon(quantity)
            added = warehouse.inventory.saldo - before
            flash(
                f"Added {format_number(added)} to {warehouse.name}.",
                "success",
            )
        return redirect(url_for("index"))

    @flask_app.post("/warehouses/<int:warehouse_id>/remove")
    def remove_stock(warehouse_id):
        warehouse = find_warehouse(warehouse_id)
        quantity = parse_positive_number(request.form.get("quantity"))
        if quantity is None:
            flash("Quantity must be a number greater than zero.", "error")
        else:
            removed = warehouse.inventory.ota_varastosta(quantity)
            flash(
                f"Removed {format_number(removed)} from {warehouse.name}.",
                "success",
            )
        return redirect(url_for("index"))

    return flask_app


def parse_positive_number(value):
    """Return a positive float or None for missing/invalid form input."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def format_number(number):
    """Avoid displaying unnecessary decimal places for whole quantities."""
    return f"{number:g}"


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
