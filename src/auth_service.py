import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.validators import validate_email, validate_password

# Ini kunci brankas token kita. (Di proyek asli, ini disimpan di file .env tersembunyi)
SECRET_KEY = "super-rahasia-uas-testing-panjang-minimal-32-byte"

class AuthService:
    def __init__(self, db):
        self.db = db

    def register(self, email, password):
        # 1. Panggil fungsi validasi super ketat yang tadi sudah lulus 100% testing
        clean_email = validate_email(email)
        clean_password = validate_password(password)
        
        # 2. Hash passwordnya!
        hashed_pw = generate_password_hash(clean_password)

        try:
            with self.db.get_conn() as conn:
                cursor = conn.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)", 
                    (clean_email, hashed_pw)
                )
                conn.commit()
                return {"success": True, "user_id": cursor.lastrowid}
        except Exception:
            # Karena email di tabel adalah UNIQUE, kalau duplikat akan lari ke sini
            raise ValueError("Email sudah terdaftar")

    def login(self, email, password):
        if not email or not password:
            raise ValueError("Email dan password harus diisi")
            
        with self.db.get_conn() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower(),)).fetchone()

        # Cek apakah user ada DAN apakah password yang diinput cocok dengan hash di database
        if not user or not check_password_hash(user['password_hash'], password):
            raise ValueError("Email atau password salah")

        # Buat "Tiket Masuk" JWT yang berlaku 24 jam
        token = jwt.encode({
            "user_id": user["id"],
            "email": user["email"],
            # exp = Waktu kadaluarsa
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        return {"success": True, "token": token}