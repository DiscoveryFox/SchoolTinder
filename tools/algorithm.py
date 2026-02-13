import typing
from tools import orm
from tools import models

class Algorithm:
    def __init__(db: orm.Database) -> None:
        pass

    def find_match(profile: models.Profile | str) -> models.Profile:
        pass

    def find_match_multiple(profile: models.Profile | str) -> list[models.Profile]:
        pass
    
    def hash_erstellen(profile: models.Profile | str):
        BucketList = []
        


    def regenerate_preferences(profile: models.Profile | str) -> None:
        """
        Raise error if something goes wrong.
        
        :param profile: Description
        :type profile: models.Profile | str
        :return: Description
        :rtype: bool
        """
        pass