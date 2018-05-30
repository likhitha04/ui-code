from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/speech/sqlalch/database.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class records(db.Model):

   __tablename__ = 'records'

   id = db.Column(db.Integer,primary_key=True)
   label = db.Column(db.String(50))
   url = db.Column(db.String(200)) 
   typeof = db.Column(db.String(20)) 
   com=db.relationship('output', backref='coms')
   def __repr__(self):
        return '<records %r>' % self.label

class userinfo(db.Model):

   __tablename__ = 'userinfo'
   id=db.Column(db.Integer,primary_key = True)
   username = db.Column( db.String(100))
   password = db.Column(db.String(100))
   role = db.Column(db.String(100))
   outputs=db.relationship('output', backref='gives')

   def __repr__(self):
        return '<userinfo %r>' % self.username


class output(db.Model):

   __tablename__ = 'output'

   id = db.Column(db.Integer, primary_key=True)
   rec_id = db.Column(db.Integer,db.ForeignKey('records.id'))
   response = db.Column(db.String(50)) 
   user_id=db.Column(db.Integer, db.ForeignKey('userinfo.id'))

   def __repr__(self):
        return '<output %r>' % self.response