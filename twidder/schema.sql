-- From serverstub.js we get the hint of three tables in total.
-- loggedinusers, users, and messages.
-- Each user has a messages field associated with itself. 
-- loggedinusers has a user associated with itself.

CREATE TABLE if not EXISTS loggedinusers(
    token VARCHAR(32) NOT NULL,
    email VARCHAR(50) NOT NULL,
    PRIMARY KEY (token)
    CONSTRAINT FK_user FOREIGN KEY (email) 
    REFERENCES users(email)
);

create table if not EXISTS users(
    email VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50),
    familyname VARCHAR(50),
    firstname VARCHAR(50),
    gender VARCHAR(50),
    password VARCHAR(50),
    PRIMARY KEY (email)
);

CREATE TABLE if not EXISTS messages(
    reciever VARCHAR(50),
    writer VARCHAR(50),
    content VARCHAR(300),
    location VARCHAR(50),
    CONSTRAINT FK_reciever FOREIGN KEY (reciever) 
    REFERENCES users(email)
);