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



query = "SELECT * " \
                "FROM Books " \
                "WHERE LOWER(authors) LIKE LOWER('%"+authors+"%') AND LOWER(publisher) LIKE LOWER('%"+publisher+ \
                "%') AND LOWER(title) LIKE LOWER('%"+title+"%') AND LOWER(subject) LIKE LOWER('%"+subject+"%');"


print query