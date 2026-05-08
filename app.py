from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

tasks = []

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route("/tasks", methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route("/tasks", methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "title is required"}), 400
    
    task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "completed": False
    }

    tasks.append(task)
    return jsonify(task), 201

if __name__ == "__main__":
    app.run(debug=True)