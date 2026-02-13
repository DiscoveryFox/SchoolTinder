from dataclasses import dataclass
from typing import Optional


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


