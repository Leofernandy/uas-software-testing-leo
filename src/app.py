from flask import Flask, request, jsonify, render_template
from functools import wraps
import jwt
from src.database import Database
from src.auth_service import AuthService, SECRET_KEY
from src.task_service import TaskService

app = Flask(__name__)

# Inisialisasi Service
db = Database()
auth_service = AuthService(db)
task_service = TaskService(db)

# --- MIDDLEWARE: Pelindung Rute (Memeriksa Token JWT) ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({"error": "Token hilang atau tidak valid!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
        except Exception:
            return jsonify({"error": "Token kadaluarsa atau tidak valid!"}), 401
            
        return f(current_user_id, *args, **kwargs)
    return decorated

# --- RUTE UTAMA (FRONTEND) ---
@app.route('/')
def index():
    return render_template('index.html')

# --- RUTE AUTHENTIKASI ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        result = auth_service.register(data.get('email'), data.get('password'))
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        result = auth_service.login(data.get('email'), data.get('password'))
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

# --- RUTE TUGAS (DILINDUNGI TOKEN) ---
@app.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user_id):
    data = request.get_json() or {}
    try:
        result = task_service.create_task(
            current_user_id,
            data.get('title'),
            data.get('description'),
            data.get('deadline')
        )
        return jsonify({"success": True, "data": result}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user_id):
    tasks = task_service.get_all_tasks(current_user_id)
    return jsonify({"success": True, "data": tasks}), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user_id, task_id):
    data = request.get_json() or {}
    try:
        result = task_service.update_task_status(current_user_id, task_id, data.get('status'))
        return jsonify(result), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user_id, task_id):
    try:
        result = task_service.delete_task(current_user_id, task_id)
        return jsonify(result), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403

if __name__ == '__main__':
    app.run(debug=True)