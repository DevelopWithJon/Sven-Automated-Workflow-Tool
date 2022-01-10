from requests.models import LocationParseError
from __init__ import db
from models import Note, Route
from utils.constants import DISTRIBUTION_CENTER_COORDINATES

import logging


try:
    import simplejson as json  # type: ignore
except:
    import json

logging.basicConfig(filename="example.log", encoding="utf-8")
LOGGER = logging.getLogger(__name__)


def display_path(route_payload: list) -> str:
    """Display routes with arrows."""
    if route_payload:
        return "".join(
            route_payload[i] + " -> "
            if i != len(route_payload) - 1
            else route_payload[i]
            for i in range(len(route_payload))
        )
    else:
        LOGGER.error("payload is empty, please check payload or debug code")
        raise ValueError


def payload_to_database(location_payload, route_payload):

    if len(route_payload) == 4:  # this means it has an alternate route
        display_altered_path = display_path(route_payload[1])
        display_shortest_full_path = display_path(route_payload[3])
        new_route = Route(
            altered_path=json.dumps(route_payload[1]),
            display_altered_path=display_altered_path,
            altered_path_value=route_payload[0],
            shortest_full_path=json.dumps(route_payload[3]),
            display_shortest_full_path=display_shortest_full_path,
            shortest_full_path_value=route_payload[2],
            alternate_route=True,
        )
    else:
        display_shortest_full_path = display_path(route_payload[1])
        new_route = Route(
            shortest_full_path=json.dumps(route_payload[1]),
            display_shortest_full_path=display_shortest_full_path,
            shortest_full_path_value=route_payload[0],
            alternate_route=False,
        )

    db.session.add(new_route)
    db.session.commit()

    # retrieve lastest route id
    route_id = db.session.query(Route).order_by(Route.id.desc()).first().id

    locations_obj = []
    for location in location_payload:
        locations_obj.append(
            Note(
                state=location["State"],
                city=location["City"],
                customer_name=location["Customer_Name"],
                product=location["Product"],
                price=location["Price"],
                units=location["Units"],
                x_coordinate=location["coordinates"][0],
                y_coordinate=location["coordinates"][1],
                route_id=route_id,
                location=location["location"],
            )
        )
    db.session.add_all(locations_obj)
    db.session.commit()


def create_map_data(routeId, location):

    data = {}
    data["location"] = location
    if Note.query.filter_by(route_id=routeId, location=location).first():
        data["x_coordinate"] = (
            Note.query.filter_by(route_id=routeId, location=location)
            .first()
            .x_coordinate
        )
        data["y_coordinate"] = (
            Note.query.filter_by(route_id=routeId, location=location)
            .first()
            .y_coordinate
        )

    else:
        data["x_coordinate"] = DISTRIBUTION_CENTER_COORDINATES[location]["x_coordinate"]
        data["y_coordinate"] = DISTRIBUTION_CENTER_COORDINATES[location]["y_coordinate"]
    return data


def query_all():
    if Route.query.all():
        for r in Route.query.all():
            r_id = r.id
            print(f"routeid: {r_id}")
            print(r.shortest_full_path)
            print(r.creation_date)
            for n in Note.query.filter_by(route_id=r_id):
                print(n.city)
    else:
        print("nothing")
