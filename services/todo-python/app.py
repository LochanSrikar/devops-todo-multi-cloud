from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests  # For calling other services later

app = Flask(__name__)
# Placeholder DB URI; update with real Azure SQL later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer)  # Links to User service

    def to_dict(self):
        return {'id': self.id, 'task': self.task, 'user_id': self.user_id}

# Create DB tables (run once)
with app.app_context():
    db.create_all()

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    # Mock User response for local testing (remove when User service is ready)
    class MockResponse:
        status_code = 200
        def json(self):
            return {'user_id': 1}

    user_response = MockResponse()
    if user_response.status_code != 200:
        return jsonify({'error': 'Unauthorized'}), 401
    new_todo = Todo(task=data['task'], user_id=user_response.json().get('user_id', 1))
    db.session.add(new_todo)
    db.session.commit()
    # Placeholder trigger for Notification (commented for now)
    # requests.post('http://localhost:5000/notify', json={'task': data['task']})
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# Add PUT and DELETE routes for practice
# @app.route('/todos/<int:id>', methods=['PUT', 'DELETE'])
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.task = data['task']
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)