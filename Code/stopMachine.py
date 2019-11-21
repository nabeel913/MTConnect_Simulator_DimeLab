import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mtconnectdatabase"]
mycol = mydb["orders"]

myquery = { "_id": "20Mach1" }
#myquery = { "PartID": "GZ" }
newvalues = { "$set": { "Order": 789789}}

mycol.update_one(myquery, newvalues)

#myquery = { "_id": "24Mach4"}
#
#mydoc = mycol.find(myquery)
#
#for x in mydoc:
#  print(x)