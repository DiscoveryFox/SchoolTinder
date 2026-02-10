import os
import sqlite3


class Database:
    """
    Database:
        - First Iteration using a sqlite connection to the database
        - Second Iteration using Connection Pooling if we still got time. 
    """
    def __init__(self, path: str):
        self.path = path
        self.scheme = """
-- Aktiviert die Unterstützung für Fremdschlüssel
PRAGMA foreign_keys = ON;

-- Tabelle: User
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Tabelle: Profile
CREATE TABLE IF NOT EXISTS Profile (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth INTEGER NOT NULL,
    gender INTEGER NOT NULL,
    home_address TEXT NOT NULL,
    hair_colour TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Tabelle: Pictures
CREATE TABLE IF NOT EXISTS Pictures (
    picture_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES Profile(profile_id) ON DELETE CASCADE
);

-- Tabelle: Preferences
CREATE TABLE IF NOT EXISTS Preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    lower_age_bound INTEGER NOT NULL,
    upper_age_bound INTEGER NOT NULL,
    sexual_preference INTEGER,
    FOREIGN KEY (profile_id) REFERENCES Profile(profile_id) ON DELETE CASCADE
);

-- Tabelle: Hobby
CREATE TABLE IF NOT EXISTS Hobby (
    hobby_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    hobby_name TEXT,
    FOREIGN KEY (profile_id) REFERENCES Profile(profile_id) ON DELETE CASCADE
);
        """

    def initialize_database(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.executescript(self.scheme)
        conn.commit()
        conn.close()
