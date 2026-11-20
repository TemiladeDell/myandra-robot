from pathlib import Path
import sqlite3

conn = sqlite3.connect("myandra.db")
with conn:
    conn.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

working_memory = {}
session_summary = ""


def load_user(user_id):
    cursor.execute("SELECT * FROM profile_memory WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

def load_learning(user_id):
    cursor.execute("SELECT topic, mastery FROM learning_memory WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def save_message(user_id, role, message):

    if user_id not in working_memory:
        working_memory[user_id] = []

    working_memory[user_id].append({
        "role": role,
        "message": message
    })

    if len(working_memory[user_id]) > 5:
        working_memory[user_id].pop(0)

    cursor.execute("""
        INSERT INTO conversation_memory (user_id, role, message)
        VALUES (?, ?, ?)
    """, (user_id, role, message))

    conn.commit()

def initialize_user_session(user_id):

    if user_id not in working_memory:

        working_memory[user_id] = load_recent_conversation(user_id)

def update_session_summary():
    global session_summary

    messages = []

    for item in working_memory:
        messages.append(item["message"])

    session_summary = " | ".join(messages)

def load_recent_conversation(user_id):

    cursor.execute("""
        SELECT role, message
        FROM conversation_memory
        WHERE user_id = ?
        ORDER BY message_id DESC
        LIMIT 5
    """, (user_id,))

    rows = cursor.fetchall()
    rows.reverse()

    return [dict(row) for row in rows]


def get_context(user_id):

    if user_id not in working_memory:
        return []

    return working_memory[user_id]

def create_user_record(name):

    cursor.execute("""
        INSERT INTO profile_memory (name)
        VALUES (?)
    """, (name,))

    conn.commit()

    return cursor.lastrowid

def search_conversation(user_id, keyword):

    cursor.execute("""
        SELECT role, message
        FROM conversation_memory
        WHERE user_id = ?
        AND LOWER(message) LIKE ?
        ORDER BY message_id DESC
        LIMIT 5
    """, (user_id, f"%{keyword.lower()}%"))

    rows = cursor.fetchall()

    return [dict(row) for row in rows]

def get_recent_dialogue(user_id):

    cursor.execute("""
        SELECT role, message
        FROM conversation_memory
        WHERE user_id = ?
        ORDER BY message_id DESC
        LIMIT 4
    """, (user_id,))

    rows = cursor.fetchall()
    rows.reverse()

    return [dict(row) for row in rows]
def save_face(user_id, face_file):

    cursor.execute("""
        INSERT OR REPLACE INTO face_memory
        (user_id, face_file)
        VALUES (?, ?)
    """, (user_id, face_file))

    conn.commit()


def load_all_faces():

    cursor.execute("""
        SELECT user_id, face_file
        FROM face_memory
    """)

    return cursor.fetchall()


# def get_difficulty(mastery):
#     if mastery < 0.3:
#         return "simple explanation"
#     elif mastery < 0.7:
#         return "guided explanation"
#     else:
#         return "advanced explanation"
