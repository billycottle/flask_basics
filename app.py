from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

app.config.update(
    SECRETKEY='#123456#',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Bc123456#@localhost:5432/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS= False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/new/')
def query_strings(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is: {0} </h1>'.format(query_val)

@app.route('/user/')
@app.route('/user/<name>')
def no_query_string(name = 'mina'):
    return '<h1> the user name is: {0} </h1>'.format(name) 

# USING TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

@app.route('/watch')
def top_movies():
    movie_list = [
        'Star Wars','ET','indiana jones', 'jaws', 'jurassic park', 'Avatar'
    ]
    return render_template('movies.html', movies=movie_list, name='Billy')

@app.route('/tables')
def movies_plus():
    movies_dict = {
        'jaws': 02.14, 'Tiburon': 1.37, 'El Chavo': 0.45, 'Kobra Kay': 3.15
    }
    return render_template('table_data.html', movies=movies_dict, name='William')


@app.route('/filters')
def filter_data():
    movies_dict = {
        'jaws': 02.14, 'tiburon': 1.37, 'el chavo': 0.45, 'kobra kay': 3.15, 'mission impossible': 1.6
    }
    return render_template('filter_data.html', movies=movies_dict, name=None, film='kobra kay') 

@app.route('/macros')
def jinja_macros():
    movies_dict = {
        'jaws': 02.14, 'tiburon': 1.37, 'el chavo': 0.45, 'kobra kay': 3.15, 'mission impossible': 1.6
    }
    return render_template('using_macros.html', movies= movies_dict)

class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'publication is {}'.format(self.name)

class Book(db.Model):


    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_page = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    #relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, format, image, num_page, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_page = num_page
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run()