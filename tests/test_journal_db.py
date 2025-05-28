import pytest
from pathlib import Path
import tempfile
import sqlite3
from src.data.journal_db import JournalDatabase

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        db_path = Path(tmp.name)
        yield db_path
        # Cleanup happens automatically when the temporary file is closed

def test_init_db(temp_db):
    """Test database initialization."""
    db = JournalDatabase(temp_db)
    
    # Verify table exists
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
        assert cursor.fetchone() is not None

def test_save_entry(temp_db):
    """Test saving entries to the database."""
    db = JournalDatabase(temp_db)
    
    # Save a test entry
    test_entry = "Test journal entry"
    test_mood = "happy"
    db.save_entry(test_entry, test_mood)
    
    # Verify entry was saved
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT entry, mood FROM entries WHERE entry = ?", (test_entry,))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == test_entry
        assert result[1] == test_mood

def test_save_empty_entry(temp_db):
    """Test that saving empty entries raises ValueError."""
    db = JournalDatabase(temp_db)
    
    with pytest.raises(ValueError):
        db.save_entry("", "happy")
    
    with pytest.raises(ValueError):
        db.save_entry("test", "")

def test_get_recent_entries(temp_db):
    """Test retrieving recent entries."""
    db = JournalDatabase(temp_db)
    
    # Add multiple entries
    entries = [
        ("Entry 1", "happy"),
        ("Entry 2", "sad"),
        ("Entry 3", "neutral"),
        ("Entry 4", "excited"),
        ("Entry 5", "calm"),
        ("Entry 6", "anxious")
    ]
    
    for entry, mood in entries:
        db.save_entry(entry, mood)
    
    # Test default limit
    recent = db.get_recent_entries()
    assert len(recent) == 5  # Default limit
    
    # Test custom limit
    recent = db.get_recent_entries(limit=3)
    assert len(recent) == 3
    
    # Verify order (most recent first)
    assert recent[0][0] == "Entry 6"
    assert recent[1][0] == "Entry 5"
    assert recent[2][0] == "Entry 4"

def test_get_entries_by_mood(temp_db):
    """Test retrieving entries by mood."""
    db = JournalDatabase(temp_db)
    
    # Add entries with different moods
    entries = [
        ("Happy entry 1", "happy"),
        ("Sad entry 1", "sad"),
        ("Happy entry 2", "happy"),
        ("Sad entry 2", "sad"),
        ("Happy entry 3", "happy")
    ]
    
    for entry, mood in entries:
        db.save_entry(entry, mood)
    
    # Test getting happy entries
    happy_entries = db.get_entries_by_mood("happy")
    assert len(happy_entries) == 3
    assert all(entry[1] == "happy" for entry in happy_entries)
    
    # Test getting sad entries
    sad_entries = db.get_entries_by_mood("sad")
    assert len(sad_entries) == 2
    assert all(entry[1] == "sad" for entry in sad_entries)
    
    # Test getting non-existent mood
    empty_entries = db.get_entries_by_mood("nonexistent")
    assert len(empty_entries) == 0 