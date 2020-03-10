# flaskproject

Voting microservice implemented using flaskapi/puglite by Matthew Nguyen

run with:

flask init

flask run

Endpoints: 

http://localhost:5000/ - home page. View all posts

/create - create a post. requires title, community, text

/total/&lt;int:id&gt; - Report the number of upvotes and downvotes for a post using post id

/upvote/&lt;int:id&gt; - Upvote a post based on post ID

/downvote/&lt;int:id&gt; - Downvote a post based on post ID

/top/&lt;int:n&gt; - List n top-scoring posts to any community

/search/?&lt;queryparameter1&gt;&&lt;queryparameter2&gt;&... - Filters posts based on query parameters and calculate score. Also sorts by score
