import pymysql
db = pymysql.connect(host='localhost',user = 'root',password= 'weisha7740',port=3306,db='test_link')
cursor = db.cursor()

# sql = """create table fitst( id int not null primary key ,name varchar(30) not null ,class_name varchar (30) not null )"""
# sql = """insert into fitst (id,name,class_name) values(1,'mike','three')"""
# sql = "update fitst set name='join' where id=1"
# sql = "delete from fitst where id =1"
sql = "select * from fitst where id=1"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    id = row[0]
    name = row[1]
    class_name = row[2]
    print(row)

# db.commit()