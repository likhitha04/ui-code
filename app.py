from flask import Flask, request, flash, url_for, redirect, render_template
from sqlalchemy import and_
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/speech/sqlalch/database.db'


db = SQLAlchemy(app)

class records(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   label = db.Column(db.String(50))
   url = db.Column(db.String(200)) 
   typeof = db.Column(db.String(20)) 
   com=db.relationship('output', backref='coms')

   def __repr__(self):
        return '<records %r>' % self.label

class userinfo(db.Model):
   id=db.Column(db.Integer,primary_key = True)
   username = db.Column( db.String(100))
   password = db.Column(db.String(100))
   role = db.Column(db.String(100))
   outputs=db.relationship('output', backref='gives')

   def __repr__(self):
        return '<userinfo %r>' % self.username


class output(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   rec_id = db.Column(db.Integer,db.ForeignKey('records.id'))
   response = db.Column(db.String(50)) 
   user_id=db.Column(db.Integer, db.ForeignKey('userinfo.id'))

   def __repr__(self):
        return '<output %r>' % self.response

@app.route('/')
def hello_world():
   return render_template('userinfo.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
 if request.method == 'POST':
        if not request.form['inputName'] or not request.form['inputPassword'] :
         flash('Please enter all the fields' , 'error')
        else:
         user= userinfo(username=request.form['inputName'], password=request.form['inputPassword'],role=request.form['role'])
         db.session.add(user)
         db.session.commit()
         return redirect(url_for('show',user=user.id))
 
@app.route('/show/<user>')
def show(user):
    
    """for rec in recos:
        var = output.query.filter(and_(output.rec_id == rec.id,output.user_id == user)).first()"""
    rid=records.query.order_by(func.random()).first().id
    rec = records.query.get(rid) 
    var = output.query.filter(and_(output.rec_id == rec.id,output.user_id == user)).first()   
    if var is None:
        return render_template('site.html',records = rec,user=user)
    else:
        return redirect(url_for('show',user=user))
    
    

@app.route('/final/<user>',methods = ['POST', 'GET'])
def final(user):
 if request.method == 'POST':
        if not request.form['pid'] or not request.form['ans'] :
         flash('Please enter all the fields' , 'error')
        else:
         some=userinfo.query.filter_by(id=user).first()
         result= output(rec_id=request.form['pid'], response=request.form['ans'],user_id= some.id)
         db.session.add(result)
         db.session.commit()
         return render_template('output.html',res=output.query.all(),user=user)
       
if __name__ == '__main__':
   app.run(debug = True)
 
