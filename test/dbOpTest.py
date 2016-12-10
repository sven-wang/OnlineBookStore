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

query = "SELECT Items.ISBN, Books.title, sum(Items.copies) \
                FROM Orders, Items, Books \
                WHERE Orders.oid = Items.oid \
                AND Items.ISBN in (SELECT distinct ISBN \
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
                AND Items.ISBN not in (SELECT  ISBN   \
	             			FROM Orders, Items  \
	               			WHERE Orders.oid = Items.oid    \
	                    	AND login_name = '" + login_name + "') \
                AND Items.ISBN = Books.ISBN \
                GROUP BY Items.ISBN \
                ORDER BY sum(copies) DESC"

print query