# ORM Usage Guide

This guide shows how to use the ORM classes in `tools/orm.py`.

## Setup

```python
from tools.orm import Database, User, Profile, Picture, Preference, Hobby

Database("schooltinder.db").initialize_database()
```

## Create Records (classmethod)

```python
user = User.create(username="alice", email="a@example.com", password="hash")
profile = Profile.create(
    user_id=user.user_id,
    first_name="Alice",
    last_name="Doe",
    date_of_birth=946684800,
    gender=1,
    home_address="Example St 1",
    hair_colour="Blond",
)
```

## Create Records (instance)

```python
user = User(username="bob", email="b@example.com", password="hash")
user.create_instance()

profile = Profile(
    user_id=user.user_id,
    first_name="Bob",
    last_name="Doe",
    date_of_birth=946684800,
    gender=0,
    home_address="Example St 2",
    hair_colour="Black",
)
profile.save()  # create if no id, update if id exists
```

## Read Records

```python
user = User.get_by_id(record_id=1)
profile = Profile.get_by_id(record_id=1)

# From instance, using stored id
profile.get()  # refresh from DB
```

## Update Records

```python
User.update_by_id(record_id=1, email="new@example.com")

profile = Profile.get_by_id(DB_PATH, 1)
profile.update(first_name="Alice", last_name="Smith")
```

## Delete Records

```python
User.delete_by_id(record_id=1)

profile = Profile.get_by_id(DB_PATH, 1)
if profile:
    profile.delete()
```

## List Records

```python
users = User.list_all()
profiles = Profile.list_all(limit=50, offset=0)
```

## User Lookup Helpers

```python
user = User.get_by_username("alice")
user = User.get_by_email("a@example.com")
user = User.get_by_login("alice")  # username or email
```

## Convert to/from Models

```python
from tools import models

user = User.get_by_id(record_id=1)
user_model = user.to_model()

user_obj = models.User(user_id=None, username="new", email="n@example.com", password="hash")
user_record = User.from_model(user_obj)
user_record.create_instance()
```

## Notes

- Each ORM operation opens a new SQLite connection.
- Foreign key enforcement is enabled per connection via `PRAGMA foreign_keys = ON`.
- `save()` creates if the id is missing, otherwise updates.
- `Database("...")` sets the default path for ORM calls that omit `db_path`.
