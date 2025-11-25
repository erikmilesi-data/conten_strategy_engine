import sqlite3
from pathlib import Path
import json
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ---- Criação da tabela principal ----
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic TEXT,
            platform TEXT,
            mode TEXT,
            users_json TEXT,
            result_json TEXT,
            username TEXT
        );
        """
    )

    # ---- Verificar se a coluna username existe ----
    cursor.execute("PRAGMA table_info(analysis_history)")
    columns = [col[1] for col in cursor.fetchall()]

    if "username" not in columns:  # adicionar apenas se faltar
        cursor.execute("ALTER TABLE analysis_history ADD COLUMN username TEXT;")

    # ---- Tabela de usuários ----
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

    # ---- Usuário padrão ----
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    row = cursor.fetchone()
    if row["total"] == 0:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin123"),
        )

    conn.commit()
    conn.close()


# ------------------------------------------------------------
#   SALVAR ANÁLISE
# ------------------------------------------------------------
def save_analysis(username: str, topic, platform, mode, users, result):
    """
    Salva a análise associada ao usuário.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history (
            timestamp,
            topic,
            platform,
            mode,
            users_json,
            result_json,
            username
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            topic,
            platform,
            mode,
            json.dumps(users, ensure_ascii=False),
            json.dumps(result, ensure_ascii=False),
            username,
        ),
    )

    conn.commit()
    conn.close()


# ------------------------------------------------------------
#   LISTAR HISTÓRICO DO USUÁRIO
# ------------------------------------------------------------
def list_history(username: str, limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, timestamp, topic, platform, mode
        FROM analysis_history
        WHERE username = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (username, limit),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------
#   CARREGAR ENTRADA ESPECÍFICA DO USUÁRIO
# ------------------------------------------------------------
def load_entry(username: str, entry_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analysis_history
        WHERE id = ? AND username = ?
        """,
        (entry_id, username),
    )

    row = cursor.fetchone()
    conn.close()
    return row


# ------------------------------------------------------------
#   BUSCAR USUÁRIO
# ------------------------------------------------------------
def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users WHERE username = ?
        """,
        (username,),
    )
    row = cursor.fetchone()
    conn.close()
    return row
