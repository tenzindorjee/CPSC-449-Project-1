-- $ sqlite3 reddit.db < reddit.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title varchar,
    community varchar,
    text varchar,
    upvote_count INT DEFAULT 0,
    downvote_count INT DEFAULT 0
);

DROP TABLE IF EXISTS upvote;
CREATE TABLE upvote (
    upvote_id INT
);

DROP TABLE IF EXISTS downvote;
CREATE TABLE downvote (
    downvote_id INT
);
COMMIT;