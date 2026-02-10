import typing
from tools import orm
from tools import models
from dataclasses import dataclass
from collections import defaultdict
import hashlib

class Algorithm:
    def __init__(self, db: orm.Database) -> None:
        self.db = db
        self.buckets = []
        self._build_index()

 
    def find_match(self, profile: models.Profile | str) -> models.Profile:
        """Find single best match"""
        matches = self.find_match_multiple(profile)
        return matches[0] if matches else None
    
    def find_match_multiple(self, profile: models.Profile | str) -> list[models.Profile]:
        """Find multiple matches ranked by score"""
        # Load profile if string ID provided
        if isinstance(profile, str):
            profile = self.db.get_profile(profile)  # Du müsstest diese Methode implementieren
        
        self.buckets.append(float(Profile.Preference.age//5))
        self.buckets.append(float(Profile.Preference.lookalike_age//6))
        if Profile.Preference.smoking == True:
            self.buckets.append(1)  
        else:
            self.buckets.append(0)  
        if Profile.Preference.drinking == True:
            self.buckets.append(1)  
        else:
            self.buckets.append(0)  

        
 
    def regenerate_preferences(self, profile: models.Profile | str) -> None:
        """
        Remove old profile from buckets and re-index with new preferences
        
        :param profile: Profile object or user_id string
        :raises ValueError: If profile not found
        """
        # Load profile if string ID provided
        if isinstance(profile, str):
            profile = self.db.get_profile(profile)
            if not profile:
                raise ValueError(f"Profile not found: {profile}")
        
        profile_id = str(profile.user_id)
        
        # Remove from all old buckets
        for bucket_name, bucket_set in self.buckets.items():
            bucket_set.discard(profile_id)
        
        # Re-index with new preferences
        self._index_profile(profile)