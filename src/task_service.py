from datetime import datetime
from src.validators import validate_title, validate_deadline

class TaskService:
    def __init__(self, db):
        self.db = db

    def _compute_is_overdue(self, deadline_str, status):
        """Menghitung apakah tugas terlambat secara real-time"""
        if not deadline_str or status == 'done':
            return False
        
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = datetime.utcnow().date()
        return today > deadline_date

    def create_task(self, user_id, title, description=None, deadline_str=None):
        # Validasi ketat
        clean_title = validate_title(title)
        clean_deadline = validate_deadline(deadline_str)
        
        with self.db.get_conn() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (user_id, title, description, status, deadline) VALUES (?, ?, ?, ?, ?)",
                (user_id, clean_title, description, 'pending', clean_deadline)
            )
            conn.commit()
            task_id = cursor.lastrowid
            
        return {
            "id": task_id,
            "title": clean_title,
            "status": "pending",
            "is_overdue": self._compute_is_overdue(clean_deadline and clean_deadline.strftime("%Y-%m-%d"), 'pending')
        }

    def get_all_tasks(self, user_id):
        # Hanya ambil tugas milik user yang sedang login
        with self.db.get_conn() as conn:
            tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
            
        result = []
        for t in tasks:
            task_dict = dict(t)
            task_dict['is_overdue'] = self._compute_is_overdue(task_dict['deadline'], task_dict['status'])
            result.append(task_dict)
            
        return result

    def update_task_status(self, user_id, task_id, new_status):
        if new_status not in ['pending', 'in_progress', 'done']:
            raise ValueError("Status tidak valid")

        with self.db.get_conn() as conn:
            # Data Isolation Check
            task = conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
            if not task:
                raise PermissionError("Tugas tidak ditemukan atau akses ditolak")

            conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
            conn.commit()
            
        return {"success": True, "message": "Status diperbarui"}

    def delete_task(self, user_id, task_id):
        with self.db.get_conn() as conn:
            # Data Isolation Check
            task = conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
            if not task:
                raise PermissionError("Tugas tidak ditemukan atau akses ditolak")

            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            
        return {"success": True, "message": "Tugas dihapus"}