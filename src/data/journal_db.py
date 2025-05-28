import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class JournalDatabase:
    def __init__(self, db_path: Path):
        """Initialize the journal database with the given path."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY,
                        entry TEXT NOT NULL,
                        mood TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def save_entry(self, entry: str, mood: str) -> None:
        """Save a journal entry to the database.
        
        Args:
            entry: The journal entry text
            mood: The detected mood
            
        Raises:
            ValueError: If entry or mood is empty
            sqlite3.Error: If database operation fails
        """
        if not entry or not mood:
            raise ValueError("Entry and mood must not be empty")
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO entries (entry, mood) VALUES (?, ?)', (entry, mood))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to save entry: {e}")
            raise
    
    def get_recent_entries(self, limit: int = 5) -> List[Tuple[str, str, str]]:
        """Get the most recent journal entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of tuples containing (entry, mood, timestamp)
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT entry, mood, timestamp FROM entries ORDER BY timestamp DESC LIMIT ?', (limit,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Failed to get recent entries: {e}")
            raise
    
    def get_entries_by_mood(self, mood: str, limit: int = 5) -> List[Tuple[str, str, str]]:
        """Get journal entries with a specific mood.
        
        Args:
            mood: The mood to filter by
            limit: Maximum number of entries to return
            
        Returns:
            List of tuples containing (entry, mood, timestamp)
            
        Raises:
            ValueError: If mood is empty
            sqlite3.Error: If database operation fails
        """
        if not mood:
            raise ValueError("Mood must not be empty")
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT entry, mood, timestamp FROM entries WHERE mood = ? ORDER BY timestamp DESC LIMIT ?', (mood, limit))
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Failed to get entries by mood: {e}")
            raise 