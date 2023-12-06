from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Endpoint for handling both GET and POST requests to /messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Retrieve messages from the database and order them by creation time
        messages = Message.query.order_by('created_at').all()

        response = make_response(
            jsonify([message.to_dict() for message in messages]),
            200,
        )
    
    elif request.method == 'POST':
        # Create a new message based on the JSON data received in the request
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        # Add the message to the database and commit the transaction
        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            201,
        )

    return response

# Endpoint for handling both PATCH and DELETE requests to /messages/<int:id>
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # Retrieve the message with the specified ID from the database
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        # Update the message attributes based on the JSON data received in the request
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
            
        # Add the updated message to the database and commit the transaction
        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            200,
        )

    elif request.method == 'DELETE':
        # Delete the message from the database and commit the transaction
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            jsonify({'deleted': True}),
            200,
        )

    return response

if __name__ == "__main__":
    app.run(port=5555)
