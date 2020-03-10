-- :name does_post_exist :scalar
SELECT COUNT(title) 
from posts 
where title = :title and community = :community and text = :text