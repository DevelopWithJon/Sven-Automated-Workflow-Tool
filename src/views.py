"""View file."""
from __init__ import db
from utils.constants import WI_STATUS
from utils.configs import MAPS_API
from utils.parse_route_data import create_map_data, payload_to_database

from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user  # type: ignore
import json
from models import Note, Route
from shortestRoute import assign_to_warehouse
from Random_Order_Generator import randomGenerator

try:
    import simplejson as json  # type: ignore
except:
    import json
views = Blueprint("views", __name__)


@views.route("/blocked", methods=["GET", "POST"])
@views.route("/completed", methods=["GET", "POST"])
@views.route("/active", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        if "add-task" in request.form:
            gen_items = request.form.get("add-task")
            try:
                gen_items = int(gen_items)
                if gen_items > 16:
                    flash(
                        "Input limit exceeded: Please submit a number under 16",
                        category="error",
                    )
                else:
                    print("generating new route...")
                    optimized_payload, assignment = assign_to_warehouse(
                        None, gen_items=gen_items
                    )
                    payload_to_database(optimized_payload, assignment)
                    flash("Sucessfully added a new task.", category="success")

            except ValueError:
                flash("Please submit a number", category="error")

    rule = request.path
    if rule == "/blocked":
        return render_template(
            "home-blocked.html",
            user=current_user,
            data=Route.query.filter(Route.status == "BLOCKED"),
        )
    elif rule == "/completed":
        return render_template(
            "home-completed.html",
            user=current_user,
            data=Route.query.filter(Route.status == "COMPLETE"),
        )
    elif rule == "/active":
        return render_template(
            "home-active.html",
            user=current_user,
            data=Route.query.filter(Route.status == "PENDING"),
        )
    else:
        return render_template(
            "home-all.html", user=current_user, data=Route.query.all()
        )


@views.route("/delete-record", methods=["POST"])
def delete_record():
    record = json.loads(request.data)
    recordId = record["RouteId"]
    locations_to_delete = Note.query.filter_by(route_id=recordId)
    for location_to_delete in locations_to_delete:
        db.session.delete(location_to_delete)
        db.session.commit()
    record_to_delete = Route.query.filter_by(id=recordId).first()
    if recordId:
        db.session.delete(record_to_delete)
        db.session.commit()

    return jsonify({})


@views.route("/workitem/<routeId>", methods=["GET", "POST"])
@login_required
def workitem(routeId):

    return render_template(
        "workitem.html",
        user=current_user,
        route_data=Route.query.filter_by(id=routeId).first(),
        locations_data=Note.query.filter_by(route_id=routeId),
        WI_STATUS=WI_STATUS,
    )


@views.route("/analyze-route/<routeId>", methods=["GET", "POST"])
@login_required
def analyze_route(routeId):

    altered = False
    removed = None

    if request.method == "POST":
        if "alter" in request.form:
            route_data = Route.query.filter_by(id=routeId).first()
            data = [
                create_map_data(routeId, location)
                for location in json.loads(route_data.altered_path)
            ]
            altered = True
            removed = list(
                set(route_data.shortest_full_path) - set(route_data.altered_path)
            )[
                0
            ]  # pull removed location by converting both lists to sets and substracting the sets

        elif "update-route" in request.form:
            update_record = Route.query.filter_by(id=routeId).first()
            update_record.shortest_full_path = update_record.altered_path
            update_record.display_shortest_full_path = (
                update_record.display_altered_path
            )
            update_record.shortest_full_path_value = update_record.altered_path_value
            update_record.altered_path = None
            update_record.display_altered_path = None
            update_record.altered_path_value = None
            update_record.alternate_route = False
            db.session.commit()

            remove = request.form.get("update-route")
            location_to_remove = Note.query.filter_by(
                route_id=routeId, location=remove
            ).first()
            db.session.delete(location_to_remove)
            db.session.commit()

            route_data = Route.query.filter_by(id=routeId).first()
            data = [
                create_map_data(routeId, location)
                for location in json.loads(route_data.shortest_full_path)
            ]
    else:
        route_data = Route.query.filter_by(id=routeId).first()
        data = [
            create_map_data(routeId, location)
            for location in json.loads(route_data.shortest_full_path)
        ]

    json_data = json.dumps(data)

    return render_template(
        "map.html",
        user=current_user,
        route_data=route_data,
        routeId=routeId,
        map_data=json_data,
        altered=altered,
        removed=removed,
        MAPS_API=MAPS_API
    )
