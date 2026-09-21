import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Note


def create_app(config_name='default'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({'message': 'Notes API is running', 'status': 'ok'})

    @app.route('/api/notes', methods=['GET'])
    def get_notes():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')

        query = Note.query
        if search:
            query = query.filter(
                Note.title.contains(search) | Note.content.contains(search)
            )

        pagination = query.order_by(Note.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'notes': [n.to_dict() for n in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
        }), 200

    @app.route('/api/notes/<int:note_id>', methods=['GET'])
    def get_note(note_id):
        note = db.session.get(Note, note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(note.to_dict()), 200

    @app.route('/api/notes', methods=['POST'])
    def create_note():
        data = request.get_json(silent=True)
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'error': 'Title and content are required'}), 400

        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201

    @app.route('/api/notes/<int:note_id>', methods=['PUT'])
    def update_note(note_id):
        note = db.session.get(Note, note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        data = request.get_json(silent=True) or {}
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify(note.to_dict()), 200

    @app.route('/api/notes/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id):
        note = db.session.get(Note, note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted'}), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)