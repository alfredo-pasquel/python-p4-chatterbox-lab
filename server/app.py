
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db

app = Flask(__name__)
CORS(app)

# Configuring the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Routes will remain here (excluding the model)
from flask import request, jsonify
from models import Message

# Initialize the database
with app.app_context():
    db.create_all()

# Routes
# GET /messages - return all messages ordered by created_at
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id> - update the message body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if message:
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200
    return jsonify({"error": "Message not found"}), 404

# DELETE /messages/<int:id> - delete the message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"}), 200
    return jsonify({"error": "Message not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
