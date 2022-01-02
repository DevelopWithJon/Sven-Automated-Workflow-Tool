from __init__ import db
from models import Note, Route
import logging

logging.basicConfig(filename='example.log', encoding='utf-8')
LOGGER = logging.getLogger(__name__)

def display_path(route_payload: list) -> str:
        """Display routes with arrows."""
        if route_payload not None:
                return "".join(route_payload[i] + "->" if i!=len(route_payload)-1 else route_payload[i] for i in range(len(route_payload)))
        else:
                LOGGER.error("payload is empty, please check payload or debug code")
                raise ValueError
        
def payload_to_database(location_payload, route_payload):
        
        if len(route_payload) == 4: # this means it has an alternate route
                altered_altered_path_value = display_path(route_payload[1])
                shortest_full_path = display_path(route_payload[3])
                new_route = Route(altered_altered_path=altered_altered_path_value, altered_altered_path_value=route_payload[0], shortest_full_path=shortest_full_path, shortest_full_path_value=route_payload[2])
        else:
                shortest_full_path = display_path(route_payload[1])
                new_route = Route(shortest_full_path=shortest_full_path, shortest_full_path_value=route_payload[0])
        
        
        db.session.add(new_route)
        db.session.commit()
        
        route_id = db.session.query(Route).order_by(Route.id).first().id
        
        locations_obj = []
        for location in location_payload:
                locations_obj.append(Note(state=location['State'], city=location['City'], customer_name=location["Customer_Name"], product=location["Product"], price=location["Price"], units=location["Units"], x_coordinate=location["coordinates"][0], y_coordinate=location["coordinates"][1], route_id=route_id))
        db.session.add_all(locations_obj)
        db.session.commit()