import pytest
import jwt
import datetime
from src.app import app, db, SECRET_KEY

# FIX: Gunakan tmp_path agar database tidak amnesia
@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True
    db_path = tmp_path / "test_api.db"
    db.db_name = str(db_path)
    db.init_db()
    with app.test_client() as client:
        yield client

def test_unauthorized_access(client):
    # 1. Tanpa Token
    res = client.get('/api/tasks')
    assert res.status_code == 401
    assert "Token hilang" in res.get_json()["error"]
    
    # 2. Token Palsu / Ngawur
    res = client.get('/api/tasks', headers={"Authorization": "Bearer TokenPalsu123"})
    assert res.status_code == 401
    
    # 3. Token Kadaluarsa (Basi)
    expired_token = jwt.encode(
        {"user_id": 1, "exp": datetime.datetime.utcnow() - datetime.timedelta(hours=1)}, 
        SECRET_KEY, algorithm="HS256"
    )
    res = client.get('/api/tasks', headers={"Authorization": f"Bearer {expired_token}"})
    assert res.status_code == 401

def test_full_api_workflow(client):
    # 1. REGISTER
    res = client.post('/api/register', json={"email": "pro@test.com", "password": "password123"})
    assert res.status_code == 201
    
    # 2. LOGIN
    res = client.post('/api/login', json={"email": "pro@test.com", "password": "password123"})
    assert res.status_code == 200
    token = res.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. CREATE TASK
    res = client.post('/api/tasks', json={"title": "Tugas API", "deadline": "2030-12-31"}, headers=headers)
    assert res.status_code == 201
    
    # 4. READ TASKS
    res = client.get('/api/tasks', headers=headers)
    assert res.status_code == 200
    tasks = res.get_json()["data"]
    assert len(tasks) == 1
    task_id = tasks[0]["id"]
    
    # 5. UPDATE TASK
    res = client.put(f'/api/tasks/{task_id}', json={"status": "done"}, headers=headers)
    assert res.status_code == 200
    
    # 6. HACKER TRY TO DELETE (Data Isolation Test)
    client.post('/api/register', json={"email": "hacker@test.com", "password": "password123"})
    hacker_token = client.post('/api/login', json={"email": "hacker@test.com", "password": "password123"}).get_json()["token"]
    res = client.delete(f'/api/tasks/{task_id}', headers={"Authorization": f"Bearer {hacker_token}"})
    assert res.status_code == 403 
    
    # 7. DELETE TASK
    res = client.delete(f'/api/tasks/{task_id}', headers=headers)
    assert res.status_code == 200

def test_api_validation_and_errors(client):
    # Register & Login cepat
    client.post('/api/register', json={"email": "err@test.com", "password": "password123"})
    token = client.post('/api/login', json={"email": "err@test.com", "password": "password123"}).get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 400 Bad Request (Judul Kosong)
    res = client.post('/api/tasks', json={"title": "   "}, headers=headers)
    assert res.status_code == 400
    
    # Setup Tugas untuk Test Update
    res = client.post('/api/tasks', json={"title": "Valid Task"}, headers=headers)
    task_id = res.get_json()["data"]["id"]
    
    # 400 Bad Request (Status Ngawur)
    res = client.put(f'/api/tasks/{task_id}', json={"status": "status_aneh"}, headers=headers)
    assert res.status_code == 400
    
    # 403 Forbidden (Hacker coba update tugas)
    client.post('/api/register', json={"email": "hacker2@test.com", "password": "password123"})
    hacker2_token = client.post('/api/login', json={"email": "hacker2@test.com", "password": "password123"}).get_json()["token"]
    res = client.put(f'/api/tasks/{task_id}', json={"status": "done"}, headers={"Authorization": f"Bearer {hacker2_token}"})
    assert res.status_code == 403

    # 500 Internal Server Error Simulation (Menghapus tabel secara paksa agar error)
    with db.get_conn() as conn:
        conn.execute("DROP TABLE tasks")
    res = client.post('/api/tasks', json={"title": "Bikin Error"}, headers=headers)
    assert res.status_code == 500


# --- TAMBAHAN INTEGRATION TEST: EDGE CASES & SECURITY ---

@pytest.mark.parametrize("endpoint, method", [
    ('/api/tasks', 'POST'),
    ('/api/tasks', 'GET'),
    ('/api/tasks/1', 'PUT'),
    ('/api/tasks/1', 'DELETE')
])
def test_api_security_no_token_all_routes(client, endpoint, method):
    # Menguji SEMUA rute memastikan mereka menolak akses jika tidak ada token
    if method == 'POST':
        res = client.post(endpoint, json={})
    elif method == 'GET':
        res = client.get(endpoint)
    elif method == 'PUT':
        res = client.put(endpoint, json={})
    else:
        res = client.delete(endpoint)
        
    assert res.status_code == 401

def test_api_malformed_json_payloads(client):
    # Register & Login
    client.post('/api/register', json={"email": "json@test.com", "password": "password123"})
    token = client.post('/api/login', json={"email": "json@test.com", "password": "password123"}).get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Kirim string kosong bukan JSON object
    res = client.post('/api/tasks', data="bukan json", headers=headers)
    # Flask by default returns 415 Unsupported Media Type atau 400 Bad Request jika JSON tidak bisa di-parse
    assert res.status_code in [400, 415] 

def test_api_method_not_allowed(client):
    # Mengirim request DELETE ke rute yang cuma nerima GET/POST
    res = client.delete('/api/register')
    assert res.status_code == 405 # Method Not Allowed