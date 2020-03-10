-- :name top_n :many
SELECT *, (upvote_count-downvote_count) as score
FROM posts
order by score DESC
LIMIT 0, :n