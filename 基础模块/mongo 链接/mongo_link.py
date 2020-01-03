import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['悟空问答']
mess = db['信息']