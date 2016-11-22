sort_key = "id"
table = "Customers"

query = "SELECT "+sort_key+" " \
                "FROM "+table+" " \
                "ORDER BY "+sort_key+" DESC " \
                "LIMIT 1"

print query