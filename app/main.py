from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length

import os
import psycopg2
import urllib.parse as urlparse

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #os.getenv('DATABASE_URL', None)
app.config['SECRET_KEY'] = 'blah' #os.getenv('WTF_KEY', None)
#db = SQLAlchemy(app)
Bootstrap(app)

class ConnectionWrapper():
  def __init__(self, connection):
    self.connection = connection

  def __del__(self):
    self.connection.close()

  def autocommit(self):
    self.connection.autocommit = True

  def cursor(self):
    return self.connection.cursor()

def ParseConfig(section_name):
  db_params = {}

  database_url  = os.getenv('DATABASE_URL', None)
  if database_url:
    parsed_url = urlparse.urlparse(database_url)
    db_params['dbname'] = parsed_url.path[1:]
    db_params['user'] = parsed_url.username
    db_params['password'] = parsed_url.password
    db_params['host'] = parsed_url.hostname
    db_params['port'] = parsed_url.port
  return db_params

def OpenDatabaseConnection(database_name):
  db_params = ParseConfig(database_name)
  return ConnectionWrapper(psycopg2.connect(**db_params))

def AddUser(name, email, zipcode):
  print("InAddUser")
  connection = OpenDatabaseConnection("user_database")
  connection.autocommit()
  cursor = connection.cursor()
  command = "INSERT INTO user_table(email, zipcode) VALUES('{}', '{}');".format(email, zipcode)
  cursor.execute(command)
  cursor.close()

class SignUpForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    zipcode = StringField('zipcode', validators=[InputRequired(), Length(min=5, max=5)])
    submit = SubmitField('Sign Up')

#class UserInfo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(50), nullable=False)
#    email = db.Column(db.String(50), unique=True, nullable=False)
#    zipcode = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignUpForm()
    if form.validate_on_submit():
        AddUser(form.name.data, form.email.data, form.zipcode.data)
        return "<h1> Success! Thank you for using Alert Alligator!<h1>"
    return render_template('index.html', form=form)

if __name__=="__main__":
    app.run(debug=True)
    
