##Jiuqi
CREATE TABLE Books(
    ISBN CHAR(13),
    title CHAR(100),
    authors VARCHAR(256),
    publisher VARCHAR(64),
    year INTEGER,
    copies INTEGER,
    price FLOAT,
    format CHAR(9) CHECK(format = 'softcover' OR format='hardcover'),
    keywords VARCHAR(100),
    subject VARCHAR(100),
    PRIMARY KEY(ISBN)
);
    

#xy
CREATE TABLE Customers(
    login_name CHAR(50) primary key,
    full_name CHAR(50),
    passwords CHAR(20),
    card_num CHAR(20),
    address CHAR(50),
    phone_num CHAR(20)
);

## Yujia
CREATE TABLE Orders( 
    login_name CHAR(50),
    ISBN CHAR(13),
    copies INTEGER,
    dateTime DATETIME,
    status CHAR(20),
    PRIMARY KEY (login_name, ISBN, dateTime),
    FOREIGN KEY (login_name) REFERENCES Customers,
    FOREIGN KEY (ISBN) REFERENCES Books
    );


## siyuan 
CREATE TABLE Feedbacks(
    fid INTEGER PRIMARY KEY,
    login_name CHAR(50),
    ISBN CHAR(13),
    dateTime DATETIME,
    score INTEGER CHECK(score >=1 AND score <= 10),
    text CHAR(200),
    FOREIGN KEY (login_name) REFERENCES Customers,
    FOREIGN KEY (ISBN) REFERENCES Books
);


##yunzhe
CREATE TABLE Rate(
    login_name CHAR(50), 
    fid INTEGER,
    usefulness INTEGER CHECK (usefulness = 0 OR usefulness = 1 OR usefulness = 2),
    PRIMARY KEY (login_name, fid),
    FOREIGN KEY (login_name) REFERENCES Customers,
    FOREIGN KEY (fid) REFERENCES Feedbacks,
    CHECK login_name IN (
        SELECT)login_name
        FROM (
            SELECT 
        WHERE 
    
);


## 1) Registration
# Yujia
INSERT INTO Customers (login_name, full_name, passwords, card_num, address, phone_num) 
VALUES (login_name, full_name, passwords, card_num, address, phone_num);

## 2) Ordering

#ViewCart Function
SELECT Books.ISBN, title, authors, publisher, year, copies, price, format, subject, copies
FROM (SELECT ISBN, copies
      FROM (SELECT MAX(oid)
            FROM Orders
            WHERE login_name = "login_name" AND status = 'Processing') o, Items i
      WHERE o.oid = i. oid) info, Books
WHERE info.ISBN = Books.ISBN


## 3) User record
#Jiuqi
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
#xy
INSERT INTO Books (ISBN, title, authors, publisher, year, copies, price, format, keywords, subject)
VALUES (ISBN, title, authors, publisher, year, copies, price, format, keywords, subject);


## 5) Arrival of more copies
#yunzhe
UPDATE Books
SET copies = 
WHERE ISBN = 

## 6) Feedback recordings
# Yujia
INSERT INTO Feedbacks (fid, cid, bid, dateTime, score, text) 
VALUES (fid, cid, bid, dateTime, score, text);

INSERT INTO Rate VALUES ('Nobody', '+ feedback_name +', '+ISBN+', 0 )

## 7) Usefulness ratings
INSERT INTO Feedbacks VALUES ('"+rater_name+"', '"+feedback_name+"', '"+ISBN+"', '"+usefulness+"');"





## 8) Book Browsing
# siyuan
# conjunctive query
SELECT * FROM Books 
WHERE LOWER(authors) LIKE LOWER("%authorName%") 
AND LOWER(publisher) = LOWER("publisher")
AND LOWER(title) = LOWER("%title%")
AND LOWER(subject) = LOWER("subject")
# sorting 

## 9) Useful feedbacks
# siyuan
SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, AVG(usefulness), Feedbacks.date FROM Rate, Feedbacks
WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = '9781449389673'
GROUP BY Rate.feedback_name ORDER BY AVG(Rate.usefulness) DESC LIMIT 5;


## 10) Book recommendation
## siyuan
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

SELECT ISBN, SUM(copies)
FROM (SELECT ISBN, copies
	  FROM Orders JOIN Items on Orders.oid = Items.oid
	  WHERE  MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
GROUP BY ISBN
ORDER BY SUM(copies) DESC
LIMIT 1

SELECT authors, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	  FROM (SELECT ISBN, copies
	  		FROM Orders o, Items i
	  		WHERE o.oid = i.oid AND MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
	  GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY authors
ORDER BY SUM(sale) DESC
LIMIT 1


SELECT publisher, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	  FROM (SELECT ISBN, copies
	  		FROM Orders o, Items i
	  		WHERE o.oid = i.oid AND MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
	  GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY publisher
ORDER BY SUM(sale) DESC
LIMIT 1