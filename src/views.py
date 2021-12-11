"""View file."""
from __init__ import db
from utils.constants import WI_STATUS
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
import json
from models import Form, Note

views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

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
    return render_template("workitem.html", user=current_user, workitem=noteId, WI_STATUS=WI_STATUS)
