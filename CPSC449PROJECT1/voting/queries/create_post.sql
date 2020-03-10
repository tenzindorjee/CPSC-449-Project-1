-- :name create_post :insert
INSERT INTO posts(title, community, text)
VALUES(:title, :community, :text)