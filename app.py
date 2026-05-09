import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "bad request"}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "internal server error"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healhty",
        "environment": os.getenv('FLASK_ENV', 'production')
    })
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({
        "tasks": [task.to_dict() for task in tasks],
        "count": len(tasks)
    })

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "request body is required"}), 400
    
    if 'title' not in data:
        return jsonify({"error": "title is required"}), 400
    
    if len(data['title'].strip()) == 0:
        return jsonify({"error": "title cannot be empty"}), 400
    
    if len(data['title']) > 200:
        return jsonify({"error": "title cannot exceed 200 characters"}), 400
    
    task = Task(title=data['title'].strip())
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "request body is required"}), 400
    
    if 'title' in data:
        if len(data['title'].strip()) == 0:
            return jsonify({"error": "title cannot be empty"}), 400
    
    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return jsonify({"error": "completed must be true or false"}), 400
        task.completed = data['completed']
    
    db.session.commit()
    return jsonify(task.to_dict())

app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "task deleted sucessfully"})

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True', port=5000)