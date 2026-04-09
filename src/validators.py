import re
from datetime import datetime

def validate_email(email):
    if not email or not isinstance(email, str):
        raise ValueError("Email tidak boleh kosong")
        
    # REGEX: Aturan baku format email sedunia (mengatasi spasi, tanpa nama, dll)
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email.strip()):
        raise ValueError("Format email tidak valid")
        
    return email.strip().lower()

def validate_password(password):
    if not password or len(password) < 8:
        raise ValueError("Password minimal 8 karakter")
    return password

def validate_title(title):
    if not title or not isinstance(title, str) or title.strip() == "":
        raise ValueError("Judul tugas tidak boleh kosong")
    if len(title) > 200:
        raise ValueError("Judul maksimal 200 karakter")
    return title.strip()

def validate_deadline(deadline_str):
    if not deadline_str:
        return None
    try:
        return datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Format deadline harus YYYY-MM-DD")