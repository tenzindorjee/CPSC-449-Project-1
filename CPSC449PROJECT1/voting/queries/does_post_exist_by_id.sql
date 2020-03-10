-- :name does_post_exist_by_id :scalar
SELECT COUNT(id) 
from posts 
where id = :id