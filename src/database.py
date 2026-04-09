import sqlite3

class Database:
    def __init__(self, db_name="app.db"):
        self.db_name = db_name
        self.init_db()

    def get_conn(self):
        conn = sqlite3.connect(self.db_name)
        # row_factory ini bikin output query jadi dictionary, bukan tuple (lebih gampang dibaca)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_conn() as conn:
            # Tabel Users
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            # Tabel Tasks
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    deadline DATE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()