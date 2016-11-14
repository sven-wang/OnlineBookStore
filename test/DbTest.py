login_name = "login_name"
full_name = "full_name"
passwords = "passwords"
card_num = "card_num"
address = "address"
phone_num = "phone_num"

ISBN = "ISBN"
title = "title"
authors = "authors"
publisher = "publisher"
year = "2015"
copies = "5"
price = "5.6"
format = "hardcover"
keywords = "algebra"
subject = "Math"


query = "UPDATE Books " \
                "SET copies = copies + "+copies+" " \
                "WHERE ISBN = '"+ISBN+"';"
print(query)
