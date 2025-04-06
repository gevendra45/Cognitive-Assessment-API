from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.journal import Journal
from app import db
from app.services.liwc_service import texttoresults
import json

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/journals', methods=['POST'])
@jwt_required()
def create_journal():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'msg': 'Journal text is required'}), 400
    dictionary = current_app.config['LIWC_DICTIONARY']
    result = texttoresults(text, dictionary)
    user_id = get_jwt_identity()
    journal = Journal(user_id=user_id, text=json.dumps(result))
    db.session.add(journal)
    db.session.commit()
    return jsonify({'journal_id': journal.id, 'score': result}), 201

@journal_bp.route('/journals/<int:journal_id>/score', methods=['GET'])
@jwt_required()
def get_score(journal_id):
    user_id = get_jwt_identity()
    journal = Journal.query.filter_by(id=journal_id, user_id=user_id).first()
    if not journal:
        return jsonify({'msg': 'Journal not found'}), 404
    scores = json.loads(journal.text)
    return jsonify({'scores': scores})
