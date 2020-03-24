from redis import StrictRedis
redis = StrictRedis(host='localhost',port=6379,db=0,password='weisha7740')
# redis.set('name','Bob')
# print(redis.get('test'))
# print(redis.exists('test'))
# redis.delete('name')
# print(redis.keys('*'))
# redis.set('name','Bob')
# print(redis.keys('*'))
# redis.rpush('test_list',1,2,3,4,)
# print(redis.llen('test_list'))
# print(redis.lrange('test_list',1,redis.llen('test_list')))
redis.sadd('n_sadd','456') #插入集合
print(redis.scard('n_sadd'))
print(redis.sismember('n_sadd','45s6')) #判断是否存在与n_sass