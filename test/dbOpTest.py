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



query = "SELECT ISBN, sum(copies) \
                FROM Orders, Items \
                WHERE Orders.oid = Items.oid \
                AND ISBN in (SELECT distinct ISBN \
                             FROM (SELECT distinct login_name \
                                    FROM Orders, Items \
                                    WHERE Orders.oid = Items.oid  \
                                    AND ISBN = '" + ISBN + "') C, Orders O, Items I \
                               WHERE c.login_name = o.login_name \
                                AND O.oid = I.oid) \
                AND Orders.login_name in (SELECT distinct login_name \
                                            FROM Orders, Items \
                                            WHERE Orders.oid = Items.oid  \
                                            AND ISBN = '" + ISBN + "') \
                GROUP BY ISBN \
                ORDER BY sum(copies) DESC"

print query