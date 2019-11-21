import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mtconnectdatabase"]
mycol = mydb["orders"]

myquery = { "PartID":'F' }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)