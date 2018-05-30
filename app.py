from flask import Flask, request, flash, url_for, redirect, render_template
from models import db,app,userinfo,records,output
from sqlalchemy import and_
from sqlalchemy import func


@app.route('/')
def hello_world():
   return render_template('userinfo.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
 if request.method == 'POST':
        if not request.form['InputName'] or not request.form['InputPassword'] :
         flash('Please enter all the fields' , 'error')
        else:
         user= userinfo(username=request.form['InputName'], password=request.form['InputPassword'],role=request.form['InputRl'])
         db.session.add(user)
         db.session.commit()
         return redirect(url_for('show',user=user.id))
 
@app.route('/show/<user>')
def show(user):
    if((output.query.filter(output.user_id == user).count())!= db.session.query(records).count()):
       rid=records.query.order_by(func.random()).first().id
       rec = records.query.get(rid) 
       var = output.query.filter(and_(output.rec_id == rec.id,output.user_id == user)).first()   
       if var is None:
          some=userinfo.query.filter_by(id=user).first()
          return render_template('site.html',records = rec,user=user,some=some)
       else:
          return redirect(url_for('show',user=user))
    else:
        return 'Completed successfully'

@app.route('/final/<user>/<rid>',methods = ['POST', 'GET'])
def final(user,rid):
 if request.method == 'POST':
        if not request.form['ans'] :
         flash('Please enter all the fields' , 'error')
        else:
         some=userinfo.query.filter_by(id=user).first()
         result= output(rec_id=rid, response=request.form['ans'],user_id= some.id)
         db.session.add(result)
         db.session.commit()
         return redirect(url_for('show',user=user))
       
if __name__ == '__main__':
   app.run(debug = True)
 
