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

CREATE TABLE Customers(
    login_name CHAR(50),
    full_name CHAR(50),
    passwords CHAR(20),
    card_num CHAR(20) UNIQUE,
    address CHAR(50),
    phone_num CHAR(20),
    PRIMARY KEY(login_name)
);

CREATE TABLE Feedbacks(
    login_name CHAR(50),
    ISBN CHAR(13),
    dateTime DATETIME,
    score INTEGER CHECK(score >=1 AND score <= 10),
    text CHAR(200),
    PRIMARY KEY (login_name, ISBN),
    FOREIGN KEY (login_name) REFERENCES Customers(login_name) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Orders(
    oid INTEGER,
    login_name CHAR(50),
    date DATE,
    status CHAR(20),
    PRIMARY KEY (oid),
    FOREIGN KEY (login_name) REFERENCES Customers(login_name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Items(
	  oid INTEGER,
    ISBN CHAR(13),
    copies INTEGER,
    PRIMARY KEY (oid, ISBN),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (oid) REFERENCES Orders(oid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Rate(
    rater_name CHAR(50),
    feedback_name CHAR(50) CHECK (feedback_name <> rater_name),
    ISBN CHAR(13),
    usefulness INTEGER CHECK (usefulness = 0 OR usefulness = 1 OR usefulness = 2),
    PRIMARY KEY (rater_name, feedback_name, ISBN),
    FOREIGN KEY (rater_name) REFERENCES Customers(login_name) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (feedback_name) REFERENCES Feedbacks(login_name) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES Feedbacks(ISBN) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Managers(
    login_name CHAR(50),
    full_name CHAR(50),
    passwords CHAR(20),
    address CHAR(50),
    phone_num CHAR(20),
    PRIMARY KEY(login_name)
);


