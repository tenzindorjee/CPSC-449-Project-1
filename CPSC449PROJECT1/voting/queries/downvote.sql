-- :name downvote :affected
UPDATE posts
SET downvote_count = downvote_count + 1
WHERE id = :id