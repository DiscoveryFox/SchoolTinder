from dataclasses import dataclass
import uuid

@dataclass
class User:
    email:str
    password:str
    user_id:uuid.UUID



@dataclass
class Preference:
    age: tuple[int, int]
    lookalike_age: tuple[int, int]
    objective_attractiveness: float
    gender: str
    body_type: str # TODO: Change to literal or class
    hobbies: list[str] # TODO: Change to literal or class
    music_taste: list[str] # TODO: Change to literal or class
    smoking: bool # TODO: Change to literal or class
    drinking: bool # TODO: Change to literal or class
    pets: list[str] # TODO: Change to literal or class
    relationship_type: str # TODO: Change to literal or class


@dataclass
class Profile:
    user_id: uuid.UUID 
    first_name: str
    last_name: str
    age: int
    lookalike_age:int,
    objective_attractiveness:float,
    gender:str
    hobbies:list[str] # TODO: Change to literal or class
    music_taste:list[str] # TODO: Change to literal or class
    smoking:bool
    drinking:bool
    pets:list[str] # TODO: Change to literal or class
    relationship_type:str # TODO: Change to literal or class
    preferences: Preference


