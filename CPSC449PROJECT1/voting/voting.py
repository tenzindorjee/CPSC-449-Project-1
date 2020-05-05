import flask_api
from flask import request, abort
from flask_api import status, exceptions
import pugsql
from dotenv import load_dotenv

load_dotenv()
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('reddit.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Home Page. Lists all posts.
# Sample curl request: curl -X GET http://localhost:5000/
@app.route('/', methods=['GET'])
def all_posts():
    all_posts = queries.all_posts()
    return list(all_posts), status.HTTP_200_OK

# Report the number of upvotes and downvotes for a post using post id
# Sample curl request: curl -X GET http://localhost:5000/total/1
@app.route('/total/<int:id>', methods=['GET'])
def report_total(id):
    return queries.report_total(id=id), status.HTTP_200_OK

# Create a post in order to upvote/downvote it
# Sample curl request: curl -X POST http://localhost:5000/create -d "title=example_title&community=example_community&text=example_text"
@app.route('/create', methods=['GET','POST'])
def create_post():
    if request.method == 'GET':
        return list(queries.all_posts()), status.HTTP_200_OK
    elif request.method == 'POST':
        return create_posts(request.data)


# Upvote a post based on post ID
# Sample curl request: curl -X PUT http://localhost:5000/upvote/1
@app.route('/upvote/<int:id>', methods=['GET','PUT'])
def upvote(id):
    if request.method == 'GET':
        return list(queries.all_posts()), status.HTTP_200_OK
    elif request.method == 'PUT':
        if (queries.does_post_exist_by_id(id=id) != 1):
            return list(queries.all_posts()), status.HTTP_404_NOT_FOUND
        else:
            queries.upvote(id=id)
            queries.create_upvote(id=id)
            return list(queries.all_posts()), status.HTTP_200_OK

# Downvote a post based on post ID
# Sample curl request: curl -X PUT http://localhost:5000/downvote/1
@app.route('/downvote/<int:id>', methods=['GET','PUT'])
def downvote(id):
    if request.method == 'GET':
        return list(queries.all_posts()), status.HTTP_200_OK
    elif request.method == 'PUT':
        if (queries.does_post_exist_by_id(id=id) != 1):
            return list(queries.all_posts()), status.HTTP_404_NOT_FOUND
        else:
            queries.downvote(id=id)
            queries.create_downvote(id=id)
            return list(queries.all_posts()), status.HTTP_200_OK

# List n top-scoring posts to any community
# Sample curl request: curl -X GET http://localhost:5000/top/1
@app.route('/top/<int:n>', methods=['GET'])
def return_top_n(n):
    return list(queries.top_n(n=n)), status.HTTP_200_OK


# Filters posts based on query parameters and calculate score. Also sort by score
# Sample curl request: curl -X GET 'http://localhost:5000/search?title=example_title&community=example_community&text=example_text'
@app.route('/search', methods=['GET'])
def post_filter():
    return filter_posts(request.args)

def create_posts(post):
    posted_fields = {*post.keys()}
    required_fields = {'title', 'community', 'text'}

    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)

    if queries.does_post_exist(post) > 0:
         return post, status.HTTP_409_CONFLICT
    else:
        post['id'] = queries.create_post(**post)
        return post, status.HTTP_201_CREATED, {'Location': f'/create/{post["id"]}'}

def filter_posts(query_parameters):
    title = query_parameters.get('title')
    community = query_parameters.get('community')
    text = query_parameters.get('text')

    query = "SELECT *, (upvote_count-downvote_count) as score FROM posts WHERE"
    to_filter = []

    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if community:
        query += ' community=? AND'
        to_filter.append(community)
    if text:
        query += ' text=? AND'
        to_filter.append(text)
    if not (title or community or text):
        raise exceptions.NotFound()

    query = query[:-4] + 'ORDER BY score DESC;'

    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results)), status.HTTP_200_OK
