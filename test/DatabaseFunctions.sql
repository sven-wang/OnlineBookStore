## 1) Registration
INSERT INTO Customers
VALUES (login_name, full_name, passwords, card_num, address, phone_num);

## 2) Ordering

#check most recent order status
SELECT status
FROM (SELECT login_name, status, oid
	  FROM Orders
  	  WHERE login_name = "login_name")
WHERE oid = MAX(oid)

# if status == 'Completed'
  # get max oid
  SELECT MAX(oid)
  FROM Orders

  # allocate new oid & get current date
  oid = oid + 1

  # insert a new order
  INSERT INTO Orders(oid, "login_name", date, "Processing")

  # insert a new item
  INSERT INTO Items(oid, "ISBN", copies)

# if status == 'Processing'
  # get current oid
  SELECT MAX(oid)
  FROM Orders
  WHERE login_name = "login_name"

  # insert new item under current oid
  INSERT INTO Items(oid, "ISBN", copies)


## 3) User record
# his/her account information 
SELECT *
FROM Customers
WHERE login_name = "login_name"

# his/her full history of orders
SELECT * 
FROM Orders
WHERE login_name = "login_name"

# his/her full history of feedbacks
SELECT *
FROM Feedbacks
WHERE login_name = "login_name"

# the list of all the feedbacks he/she ranked with respect to usefulness
SELECT *
FROM Feedback f, Rate r
WHERE r.login_name = "login_name" AND f.fid = r.fid

## 4) New book
INSERT INTO Books
VALUES (ISBN, title, authors, publisher, year, copies, price, format, keywords, subject);


## 5) Arrival of more copies
UPDATE Books
SET copies = copies + (new copies)
WHERE ISBN = "ISBN"

## 6) Feedback recordings
INSERT INTO Feedbacks
VALUES (login_name, ISBN, date, score, text) ;

INSERT INTO Rate
VALUES ('Nobody', feedback_name, ISBN, 0)

## 7) Usefulness ratings
INSERT INTO Feedbacks
VALUES (rater_name, feedback_name, ISBN, usefulness);

## 8) Book Browsing
SELECT * FROM Books 
WHERE LOWER(authors) LIKE LOWER("%author%") AND
      LOWER(publisher) LIKE LOWER("%publisher%") AND
      LOWER(title) LIKE LOWER("%title%") AND
      LOWER(subject) LIKE LOWER("%subject%")

## 9) Useful feedbacks
SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, AVG(usefulness), Feedbacks.date FROM Rate, Feedbacks
WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = '9781449389673'
GROUP BY Rate.feedback_name ORDER BY AVG(Rate.usefulness) DESC LIMIT 5;


## 10) Book recommendation
SELECT ISBN, sum(copies)
FROM Orders, Items
WHERE Orders.oid = Items.oid
AND ISBN in (SELECT distinct ISBN
             FROM (SELECT distinct login_name
             		FROM Orders, Items
               		WHERE Orders.oid = Items.oid
                    AND ISBN = "9781449389673" ) C, Orders O, Items I
               WHERE c.login_name = o.login_name
               	AND O.oid = I.oid)
AND Orders.login_name in (SELECT distinct login_name
	             			FROM Orders, Items
	               			WHERE Orders.oid = Items.oid
	                    	AND ISBN = "9781449389673")
GROUP BY ISBN
ORDER BY sum(copies) DESC

## 11) Statistics

#the list of the m most popular books
SELECT ISBN, SUM(copies)
FROM (SELECT ISBN, copies
	    FROM Orders o, Items i
	    WHERE o.oid = i.oid AND MONTH(date) = "month" AND YEAR(date) ="year" AND status = 'Complete') info
GROUP BY ISBN
ORDER BY SUM(copies) DESC
LIMIT m

#the list of m most popular authors
SELECT authors, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	    FROM (SELECT ISBN, copies
	  		    FROM Orders o, Items i
	  		    WHERE o.oid = i.oid AND MONTH(date) = "month" AND YEAR(date) = "year" AND status = 'Complete') info
	    GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY authors
ORDER BY SUM(sale) DESC
LIMIT m

#the list of m most popular publisher
SELECT publisher, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	    FROM (SELECT *
	  		    FROM Orders o, Items i
	  		    WHERE o.oid = i.oid AND MONTH(date) = "month" AND YEAR(date) = "year" AND status = 'Complete') info
	    GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY publisher
ORDER BY SUM(sale) DESC
LIMIT m