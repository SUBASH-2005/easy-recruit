import sqlite3

def save_to_db(candidate_data, match_score, is_shortlisted):
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS shortlisted (
            name TEXT,
            email TEXT,
            score REAL,
            shortlisted TEXT
        )
    ''')
    c.execute('''
        INSERT INTO shortlisted (name, email, score, shortlisted)
        VALUES (?, ?, ?, ?)
    ''', (candidate_data['name'], candidate_data['email'], match_score, 'Yes' if is_shortlisted else 'No'))
    conn.commit()
    conn.close()
    