-- :name upvote :affected
UPDATE posts
SET upvote_count = upvote_count + 1
WHERE id = :id