import sqlite3
import json
import uuid
from typing import Dict, List, Optional, Any


class CharacterDatabase:
    """
    SQLite database for storing character profiles in a NoSQL-like setup.
    Uses JSON storage for flexible document structure.
    """
    
    def __init__(self, db_path: str = "characters.db"):
        """
        Initialize the character database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with the required table structure."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create the characters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    character_id TEXT PRIMARY KEY,    -- A unique ID we generate (e.g., a UUID)
                    name TEXT NOT NULL,               -- The character's common name (e.g., "Ali")
                    disambiguation_hint TEXT,         -- A short, descriptive hint (e.g., "the merchant from Cairo")
                    profile_json TEXT                 -- JSON document containing the character profile
                );
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_characters_hint ON characters(disambiguation_hint);")
            
            conn.commit()
    
    def insert_character(self, name: str, profile: Dict[str, Any], 
                        disambiguation_hint: Optional[str] = None) -> str:
        """
        Insert a new character profile into the database.
        
        Args:
            name: Character's name
            profile: Character profile as a dictionary
            disambiguation_hint: Optional hint to distinguish between characters with same name
            
        Returns:
            The generated character_id
        """
        character_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO characters (character_id, name, disambiguation_hint, profile_json)
                VALUES (?, ?, ?, ?)
            """, (character_id, name, disambiguation_hint, json.dumps(profile)))
            conn.commit()
        
        return character_id
    
    def update_character(self, character_id: str, profile: Dict[str, Any]) -> bool:
        """
        Update an existing character profile.
        
        Args:
            character_id: The character's unique ID
            profile: Updated character profile
            
        Returns:
            True if update was successful, False if character not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE characters 
                SET profile_json = ?
                WHERE character_id = ?
            """, (json.dumps(profile), character_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a character profile by ID.
        
        Args:
            character_id: The character's unique ID
            
        Returns:
            Character profile as dictionary, or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, disambiguation_hint, profile_json
                FROM characters
                WHERE character_id = ?
            """, (character_id,))
            
            row = cursor.fetchone()
            if row:
                name, disambiguation_hint, profile_json = row
                profile = json.loads(profile_json)
                return {
                    'character_id': character_id,
                    'name': name,
                    'disambiguation_hint': disambiguation_hint,
                    'profile': profile
                }
            return None
    
    def find_characters_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Find characters by name (handles multiple characters with same name).
        
        Args:
            name: Character name to search for
            
        Returns:
            List of character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT character_id, name, disambiguation_hint, profile_json
                FROM characters
                WHERE name = ?
            """, (name,))
            
            characters = []
            for row in cursor.fetchall():
                character_id, name, disambiguation_hint, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'character_id': character_id,
                    'name': name,
                    'disambiguation_hint': disambiguation_hint,
                    'profile': profile
                })
            
            return characters
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """
        Retrieve all character profiles.
        
        Returns:
            List of all character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT character_id, name, disambiguation_hint, profile_json
                FROM characters
                ORDER BY name, disambiguation_hint
            """)
            
            characters = []
            for row in cursor.fetchall():
                character_id, name, disambiguation_hint, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'character_id': character_id,
                    'name': name,
                    'disambiguation_hint': disambiguation_hint,
                    'profile': profile
                })
            
            return characters
    
    def delete_character(self, character_id: str) -> bool:
        """
        Delete a character profile.
        
        Args:
            character_id: The character's unique ID
            
        Returns:
            True if deletion was successful, False if character not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM characters WHERE character_id = ?", (character_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_characters(self, query: str) -> List[Dict[str, Any]]:
        """
        Search characters by name or disambiguation hint.
        
        Args:
            query: Search query
            
        Returns:
            List of matching character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT character_id, name, disambiguation_hint, profile_json
                FROM characters
                WHERE name LIKE ? OR disambiguation_hint LIKE ?
                ORDER BY name, disambiguation_hint
            """, (f'%{query}%', f'%{query}%'))
            
            characters = []
            for row in cursor.fetchall():
                character_id, name, disambiguation_hint, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'character_id': character_id,
                    'name': name,
                    'disambiguation_hint': disambiguation_hint,
                    'profile': profile
                })
            
            return characters
    
    def get_character_count(self) -> int:
        """
        Get the total number of characters in the database.
        
        Returns:
            Number of characters
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM characters")
            return cursor.fetchone()[0]
    
    def clear_database(self):
        """Clear all character data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM characters")
            conn.commit()


# Global database instance
character_db = CharacterDatabase()


def get_character_db() -> CharacterDatabase:
    """Get the global character database instance."""
    return character_db 