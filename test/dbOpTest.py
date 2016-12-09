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

sortBy = 'year'
Desc_Asc = 'd'

query = "SELECT Books.ISBN, title, authors, publisher, year, copies, price, format,keywords, subject, AVG(score) \
          FROM Books natural join Feedbacks"

if (authors != ''):
    query += " WHERE LOWER(authors) LIKE LOWER('%" + authors + "%')"
    if (publisher != ''):
        query += " AND LOWER(publisher) LIKE LOWER('%" + publisher + "%')"
        if (title != ''):
            query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
        else:
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
    else:
        if (title != ''):
            query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
        else:
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
else:
    if (publisher != ''):
        query += " WHERE LOWER(publisher) LIKE LOWER('%" + publisher + "%')"
        if (title != ''):
            query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
        else:
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
    else:
        if (title != ''):
            query += " WHERE LOWER(title) LIKE LOWER('%" + title + "%')"
            if (subject != ''):
                query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
        else:
            if (subject != ''):
                query += " WHERE LOWER(subject) LIKE LOWER('%" + subject + "%')"
query += " GROUP BY Books.ISBN"
if sortBy == 'year':
    query += " ORDER BY year"
    if Desc_Asc == 'd':
        query += " Desc"
elif sortBy == 'score':
    query += " ORDER BY score"
    if Desc_Asc == 'd':
        query += ' Desc'
else:
    pass
print query