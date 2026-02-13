import tools.orm

db = tools.orm.Database("schooltinder.db")

print("test")

db.initialize_database()

profile_one = tools.orm.Profile.get_by_id(1)
preference_one = tools.orm.Preference.get_by_id

print(profile_one.to_model())
