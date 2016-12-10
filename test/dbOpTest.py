sort_key = "id"
table = "Customers"
authors = "author"
publisher = "pub"
title = "jiuqi s life"
subject = "sub"
login_name = "wsy"
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

sortBy = 'year'
Desc_Asc = 'd'
query = "SELECT Books.ISBN, title, authors, publisher, year, copies, price, format, subject, copies \
          FROM (SELECT ISBN, copies \
                FROM Items i \
                WHERE i. oid = (SELECT MAX(oid) \
                      FROM Orders \
                      WHERE login_name = '" + login_name + "' AND status = 'Processing')" \
        ") info, Books \
          WHERE info.ISBN = Books.ISBN"
print query