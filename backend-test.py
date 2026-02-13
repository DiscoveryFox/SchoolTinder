import tools.orm

db = tools.orm.Database("schooltinder.db")

print("test")

db.initialize_database()

main = tools.orm.Profile

print("test2")