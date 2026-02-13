import sqlite3
from typing import Any, Optional

from tools import models


class Database:
    """
    Database:
        - First Iteration using a sqlite connection to the database
        - Second Iteration using Connection Pooling if we still got time. 
    """
    default_path = "schooltinder.db"

    def __init__(self, path: str):
        self.path = path
        Database.default_path = path
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

    @classmethod
    def set_default_path(cls, path: str) -> None:
        cls.default_path = path

    @classmethod
    def get_default_path(cls) -> str:
        return cls.default_path


class _OrmBase:
    table: str = ""
    pk_field: str = ""
    columns: list[str] = []
    model_cls: Optional[type] = None

    def __init__(self, db_path: Optional[str] = None, **fields: Any) -> None:
        self.db_path = self._resolve_db_path(db_path)
        for name in [self.pk_field, *self.columns]:
            setattr(self, name, fields.get(name))

    @classmethod
    def _resolve_db_path(cls, db_path: Optional[str]) -> str:
        if db_path:
            return db_path
        if Database.default_path:
            return Database.default_path
        raise ValueError("Database path is required. Set Database.default_path first.")

    @classmethod
    def _connect(cls, db_path: str) -> sqlite3.Connection:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @classmethod
    def _filter_fields(cls, fields: dict[str, Any]) -> dict[str, Any]:
        return {name: value for name, value in fields.items() if name in cls.columns}

    @classmethod
    def _row_to_instance(cls, db_path: str, row: sqlite3.Row) -> "_OrmBase":
        return cls(db_path, **dict(row))

    @classmethod
    def create(cls, db_path: Optional[str] = None, **fields: Any) -> Optional["_OrmBase"]:
        db_path = cls._resolve_db_path(db_path)
        clean_fields = cls._filter_fields(fields)
        if not clean_fields:
            raise ValueError("No fields provided for create().")
        columns = ", ".join(clean_fields.keys())
        placeholders = ", ".join(["?"] * len(clean_fields))
        values = list(clean_fields.values())
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"INSERT INTO {cls.table} ({columns}) VALUES ({placeholders})",
                values,
            )
            conn.commit()
            new_id = cursor.lastrowid
        return cls.get_by_id(db_path, new_id)

    @classmethod
    def get_by_id(cls, db_path: Optional[str] = None, record_id: int = 0) -> Optional["_OrmBase"]:
        db_path = cls._resolve_db_path(db_path)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"SELECT * FROM {cls.table} WHERE {cls.pk_field} = ?",
                (record_id,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return cls._row_to_instance(db_path, row)

    @classmethod
    def list_all(
        cls, db_path: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list["_OrmBase"]:
        db_path = cls._resolve_db_path(db_path)
        query = f"SELECT * FROM {cls.table}"
        params: list[Any] = []
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
            if offset is not None:
                query += " OFFSET ?"
                params.append(offset)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        return [cls._row_to_instance(db_path, row) for row in rows]

    @classmethod
    def update_by_id(
        cls, db_path: Optional[str] = None, record_id: int = 0, **fields: Any
    ) -> Optional["_OrmBase"]:
        db_path = cls._resolve_db_path(db_path)
        clean_fields = cls._filter_fields(fields)
        if not clean_fields:
            return cls.get_by_id(db_path, record_id)
        assignments = ", ".join([f"{name} = ?" for name in clean_fields])
        values = list(clean_fields.values()) + [record_id]
        with cls._connect(db_path) as conn:
            conn.execute(
                f"UPDATE {cls.table} SET {assignments} WHERE {cls.pk_field} = ?",
                values,
            )
            conn.commit()
        return cls.get_by_id(db_path, record_id)

    @classmethod
    def delete_by_id(cls, db_path: Optional[str] = None, record_id: int = 0) -> bool:
        db_path = cls._resolve_db_path(db_path)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"DELETE FROM {cls.table} WHERE {cls.pk_field} = ?",
                (record_id,),
            )
            conn.commit()
        return cursor.rowcount > 0

    def _as_fields(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.columns}

    def _update_from_instance(self, other: "_OrmBase") -> None:
        for name in [self.pk_field, *self.columns]:
            setattr(self, name, getattr(other, name))

    def create_instance(self) -> Optional["_OrmBase"]:
        created = self.__class__.create(self.db_path, **self._as_fields())
        if created is None:
            return None
        self._update_from_instance(created)
        return self

    def create_self(self) -> Optional["_OrmBase"]:
        return self.create_instance()

    def refresh(self) -> Optional["_OrmBase"]:
        record_id = getattr(self, self.pk_field)
        if record_id is None:
            return None
        fresh = self.__class__.get_by_id(self.db_path, record_id)
        if fresh is None:
            return None
        self._update_from_instance(fresh)
        return self

    def get(self) -> Optional["_OrmBase"]:
        return self.refresh()

    def update(self, **fields: Any) -> Optional["_OrmBase"]:
        record_id = getattr(self, self.pk_field)
        if record_id is None:
            return None
        updated = self.__class__.update_by_id(self.db_path, record_id, **fields)
        if updated is None:
            return None
        self._update_from_instance(updated)
        return self

    def delete(self) -> bool:
        record_id = getattr(self, self.pk_field)
        if record_id is None:
            return False
        return self.__class__.delete_by_id(self.db_path, record_id)

    def save(self) -> Optional["_OrmBase"]:
        record_id = getattr(self, self.pk_field)
        if record_id is None:
            return self.create_instance()
        updated = self.__class__.update_by_id(self.db_path, record_id, **self._as_fields())
        if updated is None:
            return None
        self._update_from_instance(updated)
        return self

    def to_model(self) -> Optional[Any]:
        if self.model_cls is None:
            return None
        payload = {name: getattr(self, name) for name in [self.pk_field, *self.columns]}
        return self.model_cls(**payload)

    @classmethod
    def from_model(cls, model_obj: Any, db_path: Optional[str] = None) -> "_OrmBase":
        db_path = cls._resolve_db_path(db_path)
        payload = {name: getattr(model_obj, name) for name in [cls.pk_field, *cls.columns]}
        return cls(db_path, **payload)


class User(_OrmBase):
    table = "User"
    pk_field = "user_id"
    columns = ["username", "email", "password"]
    model_cls = models.User

    @classmethod
    def get_by_username(cls, username: str) -> Optional["User"]:
        db_path = cls._resolve_db_path(None)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"SELECT * FROM {cls.table} WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return cls._row_to_instance(db_path, row)

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        db_path = cls._resolve_db_path(None)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"SELECT * FROM {cls.table} WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return cls._row_to_instance(db_path, row)

    @classmethod
    def get_by_login(cls, login: str) -> Optional["User"]:
        db_path = cls._resolve_db_path(None)
        with cls._connect(db_path) as conn:
            cursor = conn.execute(
                f"SELECT * FROM {cls.table} WHERE username = ? OR email = ?",
                (login, login),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return cls._row_to_instance(db_path, row)


class Profile(_OrmBase):
    table = "Profile"
    pk_field = "profile_id"
    columns = [
        "user_id",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "home_address",
        "hair_colour",
    ]
    model_cls = models.Profile


class Picture(_OrmBase):
    table = "Pictures"
    pk_field = "picture_id"
    columns = ["profile_id", "path"]
    model_cls = models.Picture


class Preference(_OrmBase):
    table = "Preferences"
    pk_field = "preference_id"
    columns = ["profile_id", "lower_age_bound", "upper_age_bound", "sexual_preference"]
    model_cls = models.Preference


class Hobby(_OrmBase):
    table = "Hobby"
    pk_field = "hobby_id"
    columns = ["profile_id", "hobby_name"]
    model_cls = models.Hobby
