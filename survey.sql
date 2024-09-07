CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100) not null,
    lastname VARCHAR(100) not null,
    email VARCHAR(100) UNIQUE not null 
);

CREATE TABLE responses (
    id SERIAL PRIMARY KEY ,
    user_id INTEGER REFERENCES users(id) not null,
    answer1 VARCHAR(255) not null,
	answer2 VARCHAR(255) not null,
	answer3 VARCHAR(255) not null,
	answer4 VARCHAR(255) not null,
	answer5 VARCHAR(255) not null,
	answer6 VARCHAR(255) not null,
	answer7 VARCHAR(255) not null,
	answer8 VARCHAR(255) not null,
	answer9 VARCHAR(255) not null,
	answer10 VARCHAR(255) not null,
	answer11 VARCHAR(255) not null,
	answer12 VARCHAR(255) not null,
	answer13 VARCHAR(255) not null,
	answer14 VARCHAR(255) not null,
	answer15 VARCHAR(255) not null
);
select * from responses;
select * from users;



