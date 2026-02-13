import typing
from tools import orm
from tools import models
from collections import defaultdict
import math

class Algorithm:
    def __init__(self, db: orm.Database) -> None:
        self.db = db
        # Buckets: Key = bucket_id, Value = set of profile_ids
        self.buckets = defaultdict(set)
        self._build_index()
    
    def _build_index(self) -> None:
        """Build index for all profiles in database"""
        all_profiles = self.db.get_all_profiles()  # Du musst diese Methode implementieren
        for profile in all_profiles:
            self._index_profile(profile)
    
    def _profile_to_vector(self, profile: models.Profile) -> list[float]:
        """Convert profile preferences to vector"""
        vector = []
        
        # Age bucket (divided by 5)
        vector.append(float(profile.preferences.age[0] // 5))  # min age
        vector.append(float(profile.preferences.age[1] // 5))  # max age
        
        # Lookalike age bucket (divided by 6)
        vector.append(float(profile.preferences.lookalike_age[0] // 6))
        vector.append(float(profile.preferences.lookalike_age[1] // 6))
        
        # Smoking (1 or 0)
        vector.append(1.0 if profile.preferences.smoking else 0.0)
        
        # Drinking (1 or 0)
        vector.append(1.0 if profile.preferences.drinking else 0.0)
        
        # Objective attractiveness (0-10 scale, keep as is)
        vector.append(float(profile.preferences.objective_attractiveness))
        
        # Gender (encode as number: male=0, female=1, other=2, etc.)
        gender_map = {'male': 0, 'female': 1, 'other': 2, 'any': 3}
        vector.append(float(gender_map.get(profile.preferences.gender.lower(), 3)))
        
        # Body type (encode as number)
        body_map = {'slim': 0, 'athletic': 1, 'average': 2, 'curvy': 3, 'any': 4}
        vector.append(float(body_map.get(profile.preferences.body_type.lower(), 4)))
        
        # Relationship type (encode as number)
        rel_map = {'casual': 0, 'serious': 1, 'friendship': 2, 'any': 3}
        vector.append(float(rel_map.get(profile.preferences.relationship_type.lower(), 3)))
        
        # Hobbies count (simple metric)
        vector.append(float(len(profile.preferences.hobbies)))
        
        # Music taste count
        vector.append(float(len(profile.preferences.music_taste)))
        
        # Pets count
        vector.append(float(len(profile.preferences.pets)))
        
        return vector
    
    def _index_profile(self, profile: models.Profile) -> None:
        """Add profile to buckets for LSH"""
        profile_id = str(profile.user_id)
        vector = self._profile_to_vector(profile)
        
        # Create bucket keys based on different feature combinations
        # Bucket 1: Age range
        age_bucket = f"age_{int(vector[0])}_{int(vector[1])}"
        self.buckets[age_bucket].add(profile_id)
        
        # Bucket 2: Smoking + Drinking
        lifestyle_bucket = f"lifestyle_{int(vector[4])}_{int(vector[5])}"
        self.buckets[lifestyle_bucket].add(profile_id)
        
        # Bucket 3: Gender + Body type
        appearance_bucket = f"appear_{int(vector[7])}_{int(vector[8])}"
        self.buckets[appearance_bucket].add(profile_id)
        
        # Bucket 4: Relationship type
        rel_bucket = f"rel_{int(vector[9])}"
        self.buckets[rel_bucket].add(profile_id)
        
        # Bucket 5: Attractiveness range (grouped)
        attract_bucket = f"attract_{int(vector[6] // 2)}"
        self.buckets[attract_bucket].add(profile_id)
    
    def _get_candidates(self, profile: models.Profile) -> set[str]:
        """Get candidate profile IDs from buckets"""
        vector = self._profile_to_vector(profile)
        candidates = set()
        
        # Get from age bucket (including neighbors)
        for age_offset in [-1, 0, 1]:
            age_bucket = f"age_{int(vector[0]) + age_offset}_{int(vector[1]) + age_offset}"
            candidates.update(self.buckets.get(age_bucket, set()))
        
        # Get from lifestyle bucket
        lifestyle_bucket = f"lifestyle_{int(vector[4])}_{int(vector[5])}"
        candidates.update(self.buckets.get(lifestyle_bucket, set()))
        
        # Get from appearance bucket
        appearance_bucket = f"appear_{int(vector[7])}_{int(vector[8])}"
        candidates.update(self.buckets.get(appearance_bucket, set()))
        
        # Get from relationship bucket
        rel_bucket = f"rel_{int(vector[9])}"
        candidates.update(self.buckets.get(rel_bucket, set()))
        
        # Get from attractiveness bucket (including neighbors)
        for attract_offset in [-1, 0, 1]:
            attract_bucket = f"attract_{int(vector[6] // 2) + attract_offset}"
            candidates.update(self.buckets.get(attract_bucket, set()))
        
        # Remove self
        candidates.discard(str(profile.user_id))
        
        return candidates
    
    def _calculate_distance(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate Euclidean distance between two vectors"""
        # Weighted distance - some features are more important
        weights = [
            2.0,  # min age
            2.0,  # max age
            1.5,  # lookalike min age
            1.5,  # lookalike max age
            3.0,  # smoking (important!)
            2.5,  # drinking
            1.5,  # attractiveness
            2.0,  # gender
            1.0,  # body type
            2.5,  # relationship type
            0.5,  # hobbies count
            0.5,  # music count
            0.3,  # pets count
        ]
        
        distance = 0.0
        for i, (a, b) in enumerate(zip(vec1, vec2)):
            weight = weights[i] if i < len(weights) else 1.0
            distance += weight * (a - b) ** 2
        
        return math.sqrt(distance)
    
    def find_match(self, profile: models.Profile | str) -> models.Profile:
        """Find single best match"""
        matches = self.find_match_multiple(profile)
        return matches[0] if matches else None
    
    def find_match_multiple(self, profile: models.Profile | str) -> list[models.Profile]:
        """Find multiple matches ranked by score"""
        # Load profile if string ID provided
        if isinstance(profile, str):
            profile = self.db.get_profile(profile)
            if not profile:
                return []
        
        # Convert profile to vector
        my_vector = self._profile_to_vector(profile)
        
        # Phase 1: Get candidates from LSH buckets
        candidate_ids = self._get_candidates(profile)
        
        # Phase 2: Calculate distance for all candidates
        scored_matches = []
        for candidate_id in candidate_ids:
            candidate = self.db.get_profile(candidate_id)
            if not candidate:
                continue
            
            candidate_vector = self._profile_to_vector(candidate)
            distance = self._calculate_distance(my_vector, candidate_vector)
            
            # Convert distance to score (smaller distance = higher score)
            score = 1000.0 / (1.0 + distance)
            scored_matches.append((score, candidate))
        
        # Sort by score (highest first)
        scored_matches.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 20 matches
        return [match[1] for match in scored_matches[:20]]
    
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