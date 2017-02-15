# recommendation 
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
AND ISBN not in (SELECT  ISBN
	             			FROM Orders, Items
	               			WHERE Orders.oid = Items.oid
	                    	AND login_name = "1")
GROUP BY ISBN
ORDER BY sum(copies) DESC;

# statistics

SELECT ISBN, SUM(copies)
FROM (SELECT ISBN, copies
	  FROM Orders JOIN Items on Orders.oid = Items.oid
	  WHERE  MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
GROUP BY ISBN
ORDER BY SUM(copies) DESC
LIMIT 1;

SELECT authors, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	  FROM (SELECT ISBN, copies
	  		FROM Orders o, Items i
	  		WHERE o.oid = i.oid AND MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
	  GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY authors
ORDER BY SUM(sale) DESC
LIMIT 1;

SELECT AVG(usefulness) 
FROM Rate 
GROUP BY ISBN
ORDER BY AVG(usefulness) DESC 
LIMIT 1;


SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, AVG(usefulness), Feedbacks.date FROM Rate, Feedbacks 
WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = '9781449389673'
GROUP BY Rate.feedback_name ORDER BY AVG(Rate.usefulness) DESC LIMIT 5;

SELECT publisher, SUM(sale)
FROM (SELECT ISBN, SUM(copies) sale
	  FROM (SELECT ISBN, copies
	  		FROM Orders o, Items i
	  		WHERE o.oid = i.oid AND MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info
	  GROUP BY ISBN) sales, Books
WHERE sales.ISBN = Books.ISBN
GROUP BY publisher
ORDER BY SUM(sale) DESC
LIMIT 5;


SELECT Books.ISBN, title, authors, publisher, year, copies, price, format,keywords, subject, AVG(score) 
FROM Books left join Feedbacks on Books.ISBN = Feedbacks.ISBN
GROUP BY Books.ISBN
#ORDER BY year DESC
ORDER BY AVG(score) DESC;

SELECT Books.ISBN, title, authors, publisher, year, price, format, subject, info.copies           
FROM (SELECT ISBN, copies                 
FROM Items i                 
WHERE i. oid = (SELECT MAX(oid)                       
FROM Orders                       
WHERE login_name = '1' AND status = 'Processing')) info, Books           
WHERE info.ISBN = Books.ISBN;


select * from Orders;

select * from Items;


SELECT Books.ISBN, title, authors, publisher, year, price, format, subject, info.copies             FROM (SELECT ISBN, copies             FROM Items i             WHERE i. oid = (SELECT MAX(oid)             FROM Orders             WHERE login_name = 1 AND status = 'Processing')) info, Books             WHERE info.ISBN = Books.ISBN;

UPDATE Orders SET status = 'Complete' AND date = CURDATE()WHERE oid = 20160003;

SELECT status FROM (SELECT status, oid FROM Orders WHERE login_name = '1') userOrders ORDER BY oid LIMIT 1;

SELECT status, oid FROM Orders WHERE login_name = '1';

UPDATE Orders SET status = 'Complete', date = CURDATE() WHERE oid = 20160003;

SELECT oid, date, title, info.copies
FROM (SELECT oid, date, ISBN, copies
      FROM Orders o NATURAL JOIN Items i
      WHERE login_name = "1") info, Books
WHERE info.ISBN = Books.ISBN;


select * from Customers;

SELECT Items.ISBN, Books.title, sum(Items.copies)
FROM Orders, Items, Books
WHERE Orders.oid = Items.oid
AND Items.ISBN in (SELECT distinct ISBN
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
AND Books.ISBN = Items.ISBN
GROUP BY Items.ISBN
ORDER BY sum(Items.copies) DESC;

SELECT Items.ISBN, Books.title, sum(Items.copies)                 FROM Orders, Items, Books                 WHERE Orders.oid = Items.oid                 AND Items.ISBN in (SELECT distinct ISBN                              FROM (SELECT distinct login_name                                     FROM Orders, Items                                     WHERE Orders.oid = Items.oid                                      AND ISBN = 'ISBN') C, Orders O, Items I                                WHERE c.login_name = o.login_name                                 AND O.oid = I.oid)                 AND Orders.login_name in (SELECT distinct login_name                                             FROM Orders, Items                                             WHERE Orders.oid = Items.oid                                              AND ISBN = 'ISBN')                 AND Items.ISBN not in (SELECT  ISBN   	             			FROM Orders, Items  	               			WHERE Orders.oid = Items.oid    	                    	AND login_name = '1')                 AND Items.ISBN = Books.ISBN                 GROUP BY Items.ISBN                 ORDER BY sum(copies) DESC;
SELECT ISBN, copies FROM Orders o NATURAL JOIN Items i WHERE oid = '20160003';


SELECT info.ISBN, Books.title, SUM(info.copies)             FROM (SELECT ISBN, copies                   FROM Orders JOIN Items on Orders.oid = Items.oid                   WHERE  MONTH(date) = 12 AND YEAR(date) = 2016 AND status = 'Complete') info, Books             WHERE info.ISBN = Books.ISBN             GROUP BY ISBN             ORDER BY SUM(info.copies) DESC             LIMIT 3;

select ISBN, copies from Items where oid = 20160003;

SELECT status FROM (SELECT status, oid FROM Orders WHERE login_name = '') userOrders ORDER BY oid DESC LIMIT 1;


SELECT Books.ISBN, title, authors, publisher, year, price, format, subject, info.copies                     FROM (SELECT ISBN, copies                     FROM Items i                     WHERE i. oid = (SELECT MAX(oid)                     FROM Orders                     WHERE login_name = 'firstUser' AND status = 'Processing')) info, Books                     WHERE info.ISBN = Books.ISBN;

SELECT * FROM Customers WHERE login_name = 'firstUser';

SELECT oid, date, title, info.copies                     FROM (SELECT oid, date, ISBN, copies                           FROM Orders o NATURAL JOIN Items i                           WHERE login_name = firstUser) info, Books                     WHERE info.ISBN = Books.ISBN ;
select * from Books;

SELECT * FROM Feedbacks f, Rate r WHERE r.rater_name = 'firstUser' AND r.feedback_name = f.login_name AND f.ISBN = r.ISBN AND r.rater_name <> r.feedback_name;

SELECT MAX(oid)                  FROM Orders                  WHERE login_name = 'siyuan' AND status = 'Processing';


select * from Orders;

delete from Feedbacks where feedback_name = ''
