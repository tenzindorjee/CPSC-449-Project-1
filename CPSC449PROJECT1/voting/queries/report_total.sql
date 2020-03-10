-- :name report_total :one
SELECT upvote_count, downvote_count
FROM posts
where id = :id