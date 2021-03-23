DROP TABLE IF EXISTS pubmed;

CREATE TABLE pubmed (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    date DATE,
    journal VARCHAR
);
