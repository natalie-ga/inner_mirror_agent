import sqlite3
from pathlib import Path

class JournalDatabase:
    def __init__(self, db_path):
        """Initialize the journal database with the given path."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY,
                entry TEXT,
                mood TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_entry(self, entry, mood):
        """Save a journal entry to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (entry, mood) VALUES (?, ?)', (entry, mood))
        conn.commit()
        conn.close()
    
    def get_recent_entries(self, limit=5):
        """Get the most recent journal entries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT entry, mood, timestamp FROM entries ORDER BY timestamp DESC LIMIT ?', (limit,))
        entries = cursor.fetchall()
        conn.close()
        return entries
    
    def get_entries_by_mood(self, mood, limit=5):
        """Get journal entries with a specific mood."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT entry, mood, timestamp FROM entries WHERE mood = ? ORDER BY timestamp DESC LIMIT ?', (mood, limit))
        entries = cursor.fetchall()
        conn.close()
        return entries 