import pytest
from src.database import Database
from src.auth_service import AuthService

# Fixture: Fungsi yang dijalankan otomatis sebelum setiap test dimulai
@pytest.fixture
def db_memory(tmp_path):
    # Menggunakan temporary file dari pytest agar koneksi tabel tidak hilang
    db_file = tmp_path / "test_app.db"
    db = Database(str(db_file))
    yield db    

# --- TESTING REGISTRASI ---

def test_auth_register_success(db_memory):
    auth = AuthService(db_memory)
    res = auth.register("mahasiswa@kampus.com", "rahasia123")
    
    assert res["success"] is True
    assert "user_id" in res

def test_auth_register_duplicate_email(db_memory):
    auth = AuthService(db_memory)
    # Register user pertama (Berhasil)
    auth.register("dobel@kampus.com", "password123")
    
    # Register user kedua dengan email yang sama (Harus Error)
    with pytest.raises(ValueError, match="Email sudah terdaftar"):
        auth.register("dobel@kampus.com", "password123")

# --- TESTING LOGIN & JWT ---

def test_auth_login_success(db_memory):
    auth = AuthService(db_memory)
    auth.register("login@kampus.com", "password123")
    
    # Mencoba login dengan data yang benar
    res = auth.login("login@kampus.com", "password123")
    assert res["success"] is True
    assert "token" in res  # Pastikan tiket JWT berhasil dibuat

def test_auth_login_failed(db_memory):
    auth = AuthService(db_memory)
    auth.register("hacker@kampus.com", "password123")
    
    # Skenario 1: Password salah
    with pytest.raises(ValueError, match="Email atau password salah"):
        auth.login("hacker@kampus.com", "salahpass")
        
    # Skenario 2: Email tidak terdaftar
    with pytest.raises(ValueError, match="Email atau password salah"):
        auth.login("siapa_ini@kampus.com", "password123")
        
    # Skenario 3: Input kosong
    with pytest.raises(ValueError, match="Email dan password harus diisi"):
        auth.login("", "")