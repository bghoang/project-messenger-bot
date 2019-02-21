from mbdb import MBDataBase

db = MBDataBase("Kaus u suck")
user ={"Bao": "player"}
db.create_user(123, user)
#db.load_database("result.txt")
print(db)
