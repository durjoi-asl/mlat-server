from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/testThings'
# app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False
app.debug = True

FLASKHOST = "localhost"
FLASKPORT = 5001 # port of flask hosting
DEBUGTRUTH = True # whether in debug mode or not

db = SQLAlchemy(app)

class books(db.Model):
    __tablename__='books'
    bookTitle = db.Column(db.String(100), primary_key=True)
    bookText = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer(), default=0)

    def __init__(self, bookTitle, bookText, likes) -> None:
        self.bookTitle = bookTitle
        self.bookText = bookText
        self.likes = likes

@app.route('/test', methods=['GET'])
def test():
    return {
        'test':'test'
    }

if __name__ == "__main__":
    db.create_all()
    app.run(host=FLASKHOST, port=FLASKPORT, debug=DEBUGTRUTH)
