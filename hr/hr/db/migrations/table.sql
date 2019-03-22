CREATE TABLE jobs
(
  id    serial PRIMARY KEY,
  date  VARCHAR(400) NOT NULL,
  text  TEXT,
  ref   VARCHAR(200),
  url   VARCHAR(400) UNIQUE NOT NULL ,
  email VARCHAR(400)
)