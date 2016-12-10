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

query = "SELECT * " \
                 "FROM Feedbacks f, Rate r " \
                 "WHERE r.rater_name = " + "'" + login_name + "' AND r.feedback_name = f.login_name AND f.ISBN = r.ISBN AND r.rater_name <> r.feedback_name;"


print query