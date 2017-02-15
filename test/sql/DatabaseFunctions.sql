

## 1) Registration
INSERT INTO Customers
VALUES (login_name, full_name, passwords, card_num, address, phone_num);

## 2) Ordering
# Ordering Function
#check most recent order status

SELECT status FROM (SELECT status, oid FROM Orders WHERE login_name = '1') userOrders
ORDER BY oid Desc
LIMIT 1;

# if status == 'Completed'
# get max oid
SELECT MAX(oid)
FROM Orders
# allocate new oid & get current date
oid = oid + 1
# insert a new order
INSERT INTO Orders(oid, "login_name", date, "Processing")
# insert a new item
INSERT INTO Items(oid, "ISBN", copies);

# if status == 'Processing'
# get current oid
SELECT MAX(oid)
FROM Orders
WHERE login_name = "login_name";
# insert new item under current oid
INSERT INTO Items VALUES (oid, "ISBN", copies);

#ViewCart Function
SELECT Books.ISBN, title, authors, publisher, year, copies, price, format, subject, copies
FROM (SELECT ISBN, copies
      FROM (SELECT MAX(oid)
            FROM Orders
            WHERE login_name = "login_name" AND status = 'Processing') o, Items i
      WHERE o.oid = i. oid) info, Books
WHERE info.ISBN = Books.ISBN;

# Checkout function
## update order status
UPDATE Orders
SET status = 'Complete', date = CURDATE()
WHERE oid = oidLong;
## queryOrders
select ISBN, copies from Items where oid = oidLong;
## updateBookCopies: for item in orders
UPDATE Books
SET copies = copies - 'copiesINT'
WHERE ISBN = 'ISBNchar';


## 3) User record
# his/her account information
SELECT *
FROM Customers
WHERE login_name = "login_name";

# his/her full history of orders
SELECT oid, date, title, info.copies
FROM (SELECT oid, date, ISBN, copies
      FROM Orders o NATURAL JOIN Items i
      WHERE login_name = "login_name") info, Books
WHERE info.ISBN = Books.ISBN;

# his/her full history of feedbacks
SELECT *
FROM Feedbacks
WHERE login_name = "login_name";

# the list of all the feedbacks he/she rated
SELECT *
FROM Feedbacks f, Rate r
WHERE r.rater_name = 'login_name'
      AND r.feedback_name = f.login_name
      AND f.ISBN = r.ISBN
      AND r.rater_name <> r.feedback_name;


## 4) New book
INSERT INTO Books
VALUES (ISBN, title, authors, publisher, year, copies, price, format, keywords, subject);


## 5) Arrival of more copies
UPDATE Books
SET copies = copies + 'newCopiesINT'
WHERE ISBN = "ISBN";



## 6) Feedback recordings
INSERT INTO Feedbacks
VALUES ('login_name', 'ISBN', CURDATE(), 'score', 'text') ;

INSERT INTO Rate
VALUES ('feedback_name', 'feedback_name', 'ISBN', 0);

## 7) Usefulness ratings
INSERT INTO Feedbacks
VALUES ('rater_name', 'feedback_name', 'ISBN', 'usefulness');

## 8) Book Browsing
SELECT Books.ISBN, title, authors, publisher, year, copies, price, format,keywords, subject, AVG(score)
FROM Books left join Feedbacks on Books.ISBN = Feedbacks.ISBN
WHERE LOWER(authors) LIKE LOWER("%author%") AND
      LOWER(publisher) LIKE LOWER("%publisher%") AND
      LOWER(title) LIKE LOWER("%title%") AND
      LOWER(subject) LIKE LOWER("%subject%")
GROUP BY Books.ISBN
ORDER BY year DESC
  OR
ORDER BY AVG(score) DESC;


## 9) Useful feedbacks
SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, ROUND(AVG(usefulness),1), Feedbacks.date
FROM Rate, Feedbacks
WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = "ISBN"
GROUP BY Rate.feedback_name
ORDER BY AVG(Rate.usefulness)
DESC LIMIT n;



## 10) Book recommendation
SELECT Items.ISBN, Books.title, sum(Items.copies)
FROM Orders, Items, Books
WHERE Orders.oid = Items.oid
      AND Items.ISBN in (SELECT distinct ISBN
                         FROM (SELECT distinct login_name
                               FROM Orders, Items
                               WHERE Orders.oid = Items.oid
                                     AND ISBN = 'ISBN') C, Orders O, Items I
                         WHERE c.login_name = o.login_name AND O.oid = I.oid)
      AND Orders.login_name in (SELECT distinct login_name
                                FROM Orders, Items
                                WHERE Orders.oid = Items.oid
                                      AND ISBN = 'ISBN')
      AND Items.ISBN not in (SELECT ISBN
        	             			 FROM Orders, Items
        	               		 WHERE Orders.oid = Items.oid
                                   AND login_name = 'login_name')
      AND Items.ISBN = Books.ISBN
GROUP BY Items.ISBN
ORDER BY sum(copies) DESC;





## 11) Statistics

#the list of the m most popular books


SELECT info.ISBN, Books.title, SUM(info.copies)
FROM (SELECT ISBN, copies
      FROM Orders JOIN Items on Orders.oid = Items.oid
      WHERE  MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info, Books
WHERE info.ISBN = Books.ISBN
GROUP BY ISBN
ORDER BY SUM(info.copies) DESC
LIMIT m;


#the list of m most popular authors
SELECT authors, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	    FROM (SELECT ISBN, copies
	  		    FROM Orders o, Items i
	  		    WHERE o.oid = i.oid AND MONTH(date) = 'month' AND YEAR(date) = 'year' AND status = 'Complete') info
	    GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY authors
ORDER BY SUM(sale) DESC
LIMIT m;

#the list of m most popular publisher
SELECT publisher, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
      FROM (SELECT ISBN, copies
            FROM Orders o, Items i
            WHERE o.oid = i.oid AND MONTH(date) = 'month' AND YEAR(date) = 'year' AND status = 'Complete') info
      GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY publisher
ORDER BY SUM(sale) DESC
LIMIT m;