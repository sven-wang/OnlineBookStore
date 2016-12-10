sort_key = "id"
table = "Customers"
authors = "author"
publisher = "pub"
title = "jiuqi s life"
subject = "sub"
login_name = "firstUser"
ISBN = "ISBN"
dateTime = "12-12-1996"
score = "4"
text = "zhen hao a!"
n = 5
year = '2016'
month = 12
m = 3
price = '10'
keywords = 'life'
copies = '1'
format = 'softcover'
oid = '20160003'

sortBy = 'year'
Desc_Asc = 'd'

query = "SELECT oid, date, title, info.copies \
                    FROM (SELECT oid, date, ISBN, copies \
                          FROM Orders o NATURAL JOIN Items i \
                          WHERE login_name = " + login_name + ") info, Books \
                    WHERE info.ISBN = Books.ISBN "

print query