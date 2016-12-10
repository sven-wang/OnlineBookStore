sort_key = "id"
table = "Customers"
authors = "author"
publisher = "pub"
title = "jiuqi s life"
subject = "sub"
login_name = "1"
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

query = "UPDATE Orders " \
        "SET status = 'Complete' AND date = CURDATE() " + \
        "WHERE oid = " + oid

print query