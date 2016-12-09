sort_key = "id"
table = "Customers"
authors = "wsy"
publisher = "wyj"
title = "hahaha"
subject = "sub"
login_name = "wsy"
ISBN = "123456"
dateTime = "12-12-1996"
score = "4"
text = "zhen hao a!"
n = 5
year = 2016
month = 12
m = 3

query = "SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, AVG(usefulness), Feedbacks.date FROM Rate, Feedbacks \
          WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = '" + ISBN + "' GROUP BY Rate.feedback_name ORDER BY AVG(Rate.usefulness) DESC LIMIT " + str(n)

print query