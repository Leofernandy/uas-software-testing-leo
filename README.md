# 🚀 ProTask Manager
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)
[![codecov](https://codecov.io/github/Leofernandy/uas-software-testing-leo/graph/badge.svg?token=HVUJ3CTAU3)](https://codecov.io/github/Leofernandy/uas-software-testing-leo)
![Tests](https://img.shields.io/badge/Tests-Passing-success)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

Aplikasi manajemen tugas berbasis **Flask (backend)** dan **Modern Vanilla JavaScript + Bootstrap (frontend)** yang dirancang dengan fokus pada **kualitas perangkat lunak**, menggunakan pendekatan **Test-Driven Development (TDD)** dan target **100% test coverage**.

---

## 📋 Deskripsi Sistem

**ProTask Manager** membantu pengguna mengelola tugas secara efisien dengan fitur utama:

- ✅ **Manajemen Tugas (CRUD)**  
  Membuat, membaca, memperbarui, dan menghapus tugas dengan atribut:
  - Judul
  - Deskripsi
  - Deadline
  - Status dinamis

- 📊 **Dashboard Produktivitas**  
  Visualisasi statistik tugas secara real-time:
  - Total Tasks
  - Pending
  - Active (In Progress)
  - Done

- 🔐 **Keamanan JWT Authentication**  
  Menggunakan JSON Web Token (HS256) untuk memastikan:
  - Autentikasi aman
  - Isolasi data antar pengguna

- 🔔 **Sistem Notifikasi Modern**  
  Integrasi **SweetAlert2** untuk feedback interaksi pengguna yang interaktif

---

## 🏛️ Arsitektur Aplikasi

```plaintext
uas-software-testing-leo/
├── src/
│   ├── app.py              # Entry point: Routing API & Middleware JWT
│   ├── database.py         # SQLite connection wrapper
│   ├── auth_service.py     # Business logic: register & login
│   ├── task_service.py     # Business logic: task & overdue engine
│   ├── validators.py       # Input validation (regex & business rules)
│   └── templates/          # Frontend SPA (HTML, JS, Bootstrap)
│
├── tests/
│   ├── test_services.py     # Unit test: business logic
│   ├── test_validators.py   # Unit test: input validation & edge cases
│   └── test_integration.py  # Integration test: API + database flow
│
├── .github/workflows/
│   └── ci.yml              # CI pipeline (GitHub Actions)
│
├── requirements.txt        # Dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # Project documentation
```

---

## 💻 Stack Teknologi

| Bagian        | Teknologi |
|--------------|----------|
| Backend       | Python 3.11, Flask, SQLite |
| Frontend      | JavaScript (ES6+), Bootstrap 5, SweetAlert2 |
| Autentikasi   | JWT (PyJWT) |
| Testing       | Pytest, Pytest-Cov, Hypothesis |
| CI/CD         | GitHub Actions |

---

## ⚙️ Cara Menjalankan Aplikasi

### 1. Instalasi

```bash
# Clone repository
git clone https://github.com/username/uas-software-testing-leo.git
cd uas-software-testing-leo

# Buat virtual environment
python3 -m venv venv

# Aktifkan environment
# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Menjalankan Server

```bash
python -m src.app
```

Akses aplikasi di:
```
http://localhost:5000
```

---

## 🧪 Strategi Pengujian

### 🎯 Target: 100% Test Coverage

Semua logika backend dalam folder `src/` wajib memiliki cakupan pengujian penuh.

---

### ▶️ Menjalankan Testing

```bash
pytest --cov=src --cov-report=term-missing
```

---

## 🔍 Kategori Pengujian

### ✅ Unit Testing
- Menguji `validators.py`:
  - Format email
  - Validasi judul kosong
- Menguji `task_service.py`:
  - Logika status overdue
  - Perubahan status task

---

### 🔗 Integration Testing
- Menggunakan `Flask test_client`
- Simulasi alur lengkap:
  1. Register
  2. Login
  3. Create Task
  4. Update Task
  5. Delete Task

---

### 🔐 Security Testing
- Endpoint tanpa token → **401 Unauthorized**
- Akses task user lain → **403 Forbidden**

---

### 🔁 Property-Based Testing
- Menggunakan **Hypothesis**
- Menguji validator dengan:
  - Ratusan input acak
  - Edge cases ekstrem

---

## 📡 Dokumentasi API

### Base URL
```
http://localhost:5000/api
```

---

### 🔑 Auth Endpoints

| Method | Endpoint   | Deskripsi                  | Status |
|--------|------------|---------------------------|--------|
| POST   | /register  | Registrasi user baru      | 201    |
| POST   | /login     | Login & mendapatkan token | 200    |

---

### 📌 Task Endpoints (Protected)

| Method | Endpoint        | Deskripsi                      | Status |
|--------|----------------|-------------------------------|--------|
| GET    | /tasks         | Ambil semua task user         | 200    |
| POST   | /tasks         | Tambah task baru              | 201    |
| PUT    | /tasks/{id}    | Update status task            | 200    |
| DELETE | /tasks/{id}    | Hapus task                    | 200    |

---

## 🛠️ Penanganan Error

| Status Code | Keterangan |
|------------|-----------|
| 400 | Bad Request → Input tidak valid |
| 401 | Unauthorized → Token tidak ada / invalid |
| 403 | Forbidden → Akses resource milik user lain |
| 500 | Internal Server Error |

---

## 📌 Catatan Pengembangan

- Menggunakan pendekatan **TDD (Test-Driven Development)**
- Setiap fitur harus:
  1. Ditulis test terlebih dahulu
  2. Implementasi kode
  3. Refactor dengan tetap lulus test

---

## 👨‍💻 Author

**Leo Fernandy**  
📅 2026  
🎓 UAS Software Testing Project

---

## 📜 Lisensi

Project ini dibuat untuk keperluan akademik dan pembelajaran.
