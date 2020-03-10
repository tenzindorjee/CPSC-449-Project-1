curl -X GET http://localhost:5000

curl \
    --header "Content-type: application/json" \
    --request POST \
    --data '{"title":"example_title","community":"example_community","text":"example_text"}' \
    http://localhost:5000/create

curl \
    --header "Content-type: application/json" \
    --request PUT \
    http://localhost:5000/upvote/1

curl \
    --header "Content-type: application/json" \
    --request PUT \
    http://localhost:5000/downvote/50