"""View file."""
from __init__ import db
from utils.constants import WI_STATUS
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
import json
from models import Form, Note
from shortestRoute import assign_to_warehouse
from utils.parse_route_data import payload_to_database

views = Blueprint("views", __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if "note" in request.form:
            note = request.form.get('note')

            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        elif "Random_Order_Generator" in request.form:
            gen_items = request.form.get("Random_Order_Generator")
            
            try: 
                gen_items = int(gen_items)
            except ValueError:
                flash('Please submit a number', category='error')
                raise ValueError
            
            optimized_payload, assignment = assign_to_warehouse(None, gen_items=gen_items)
            payload_to_database(optimized_payload, assignment)

            
        
        
    

    return render_template("home.html", user=current_user, data=Note.query.all())

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note_to_delete = Note.query.get(noteId)
    if noteId:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()

    return jsonify({})

@views.route('/workitem/<noteId>', methods=['GET', 'POST'])
@login_required
def workitem(noteId):
    return render_template("workitem.html", user=current_user, workitem=noteId, data=Note.query.filter_by(id=noteId).first(), WI_STATUS=WI_STATUS)

@views.route('/maps', methods=['GET', 'POST'])
def maps():
    return render_template("map.html", user=current_user, workitem=noteId, WI_STATUS=WI_STATUS)

@views.route('random_order', methods=['GET, POST'])
@login_required
def random_order():
    return render_template('')

@views.route('/add_routes', methods=['POST'])
def add_routes():
   pass