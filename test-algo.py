import tools.algo
import tools.orm

db = tools.orm.Database("test.sqlite")


a = tools.algo.Algorithm(db)

a.find_match()