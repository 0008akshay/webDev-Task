from flask import Flask,render_template,request,flash,redirect,url_for
from forms import ContactForm
from flask_mail import Mail,Message
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
import os
basedir=os.path.abspath(os.path.dirname(__file__))


mail=Mail()
app=Flask(__name__)

app.secret_key = 'development key'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(basedir,'Data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
db.init_app(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX']='[FLASK APP]'
app.config['MAIL_SENDER']='ADMIN <webdevtask2021@gmail.com>'

def send_mail_async(app,msg):
  with app.app_context():
    mail.send(msg)


def send_mail(to,subject,template,**kwargs):
  msg=Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_SENDER'],recipients=[to])
  msg.body=render_template(template + '.txt',**kwargs)
  msg.html=render_template(template + '.html',**kwargs)
  thr=Thread(target=send_mail_async,args=[app,msg])
  thr.start()
  return thr

class user(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120),nullable=False)
  subject = db.Column(db.String(200), nullable=False)
  message = db.Column(db.String(500), nullable=False)
  def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.subject}','{self.message}')"

mail.init_app(app)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate_on_submit == False:
      return render_template('contact.html', form=form)
    else:
      name=request.form.get('name')
      email=request.form.get('email')
      subject=request.form.get('subject')
      message=request.form.get('message')
      entry=user(username=name,email=email,subject=subject,message=message)
      db.session.add(entry)
      db.session.commit()
      send_mail(app.config['MAIL_USERNAME'],'NEW USER','mail/new_user',user=entry)
      flash('Thanks for Submiting your query')
      return redirect(url_for('contact'))
  elif request.method == 'GET':
     return render_template('contact.html', form=form)  