import sqlite3
from flask import Flask, g, request, Response, json, jsonify
from functools import wraps

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

DATABASE = 'database.db'

############DATABASE HELPERS#####################
def init_db():
    print(DATABASE)
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    get_db().commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert(table, fields=(), values=()):
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur = get_db().execute(query, values)
    get_db().commit()
    id = cur.lastrowid
    cur.close()
    return id

##################AUTHENTICATION#####################
def check_auth(username, password):
    users = query_db('select * from users where username="%s" AND password="%s"' % (username, password))
    return len(users)!=0

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Resouce requires authentication'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

##################ROUTES#####################
@app.route('/movies', methods = ['GET', 'POST'])
@requires_auth
def movies():
    data = []
    if request.method == 'GET':
        for movie in query_db('select * from movies'):
            data.append(movie)

    if request.method == 'POST':
        data = dict(request.json)
        values = (data['title'], data['description'], data['director'], data['year'], data['rating'])
        insert('movies', ('title', 'description', 'director', 'year', 'rating'), values)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/movie/<movie_id>', methods = ['GET', 'PATCH', 'DELETE'])
def movie(movie_id):
    if request.method == 'GET':
        movie = query_db('select * from movies WHERE id = ?', movie_id)

    if request.method == 'DELETE':
        movie = query_db('delete from movies WHERE id = ?', movie_id)

    if request.method == 'PATCH':
        data = dict(request.json)
        values=""
        for attribute in data:
            values+='%s = "%s",' % (attribute, data[attribute])
        values = values[:-1]
        movie = query_db("update movies set " + values + " WHERE id = ?", movie_id)
    
    resp = Response(json.dumps(movie), status=200, mimetype='application/json')
    return resp

@app.route('/users', methods = ['POST'])
def users():
    data = []
    if request.method == 'POST':
        data = dict(request.json)
        values = (data['username'], data['password'])
        insert('users', ('username', 'password'), values)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')