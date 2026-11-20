from myandradb_link import cursor, conn

def save_fact(user_id, category, value):

    cursor.execute("""
        INSERT INTO known_facts(user_id, category, value)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, category)
        DO UPDATE SET value = excluded.value
    """, (user_id, category, value))

    conn.commit()


def get_facts(user_id):

    cursor.execute("""
        SELECT category, value
        FROM known_facts
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    return [dict(row) for row in rows]
