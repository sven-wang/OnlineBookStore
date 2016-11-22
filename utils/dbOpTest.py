sort_key = "id"
table = "Customers"
authors = "wsy"
publisher = "wyj"
title = "hahaha"
subject = "sub"



query = "SELECT * " \
                "FROM Books " \
                "WHERE authors = " + "'"+authors+"' AND publisher = '"+publisher+ \
                "' AND title = '"+title+" AND subject = '"+subject+"' ;"

print query