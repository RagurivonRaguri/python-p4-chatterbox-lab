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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
       messages = Message.query.order_by(Message.created_at.asc()).all()

       message_dict = []
       for message in messages:
        dicted = message.to_dict()
        message_dict.append(dicted)
    
        response = make_response(
          jsonify(message_dict),
          200
        )
        return response
       
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            201,
        )
    return response


@app.route('/messages/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def messages_by_id(id):
    if request.method == 'GET':
        message = Message.query.filter_by(id=id).first()
        dicted = message.to_dict()
        response = make_response(
            jsonify(dicted),
            200
        )
        return response

    elif request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response

    elif request.method == 'PATCH':
      message = Message.query.filter_by(id=id).first()
      data = request.get_json()
      message.body = data['body']
      db.session.commit()

      response = make_response(
        jsonify(message.to_dict()),
        200,
        )
      return response

if __name__ == '__main__':
    app.run(port=5555)
