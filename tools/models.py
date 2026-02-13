from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email:str
    password:str
    user_id:uuid.UUID



@dataclass
class User:
    user_id: Optional[int]
    username: str
    email: str
    password: str


@dataclass
class Profile:
    profile_id: Optional[int]
    user_id: int
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
    date_of_birth: int
    gender: int
    home_address: str
    hair_colour: str


@dataclass
class Picture:
    picture_id: Optional[int]
    profile_id: int
    path: str


@dataclass
class Preference:
    preference_id: Optional[int]
    profile_id: int
    lower_age_bound: int
    upper_age_bound: int
    sexual_preference: Optional[int]


@dataclass
class Hobby:
    hobby_id: Optional[int]
    profile_id: int
    hobby_name: Optional[str]


