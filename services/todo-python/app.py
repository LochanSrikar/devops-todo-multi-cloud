from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests  # For calling other services
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows all origins for local testing
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
    # Real call to User service (assume it's running on localhost:8080)
    try:
        user_response = requests.get('http://host.docker.internal:8080/api/users/verify', params={'token': data.get('token', 'test')})
        if user_response.status_code != 200:
            return jsonify({'error': 'Unauthorized'}), 401
        user_data = user_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'User service unavailable'}), 503  # Service unavailable error

    new_todo = Todo(task=data['task'], user_id=user_data.get('user_id', 1))
    db.session.add(new_todo)
    db.session.commit()

    # Trigger Notification service (placeholder; update URL in Step 4)
    try:
        requests.post('http://localhost:5098/notify', json={'task': data['task']})
    except requests.exceptions.RequestException as e:
        # Log error but don't fail the todo creation
        print(f"Notification failed: {e}")

    return jsonify(new_todo.to_dict()), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

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