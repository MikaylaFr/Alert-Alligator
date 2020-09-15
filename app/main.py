from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, Length
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', None) #'sqlite:///test.db'
app.config['SECRET_KEY'] = os.getenv('WTF_KEY', None)
db = SQLAlchemy(app)
Bootstrap(app)

class SignUpForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('email', validators=[InputRequired(), Email(message='Valid email required.'), Length(min=5, max=50)])
    zipcode = StringField('zipcode', validators=[InputRequired(), Length(min=5, max=5)])

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignUpForm()
    if form.validate_on_submit():
        newUser = UserInfo(name = form.name.data, email = form.email.data, zipcode = form.zipcode.data)
        db.session.add(newUser)
        db.session.commit()
        return "<h1> Success! Thank you for using Alert Alligator!<h1>"
    return render_template('index.html', form=form)

if __name__=="__main__":
    app.run(debug=True)
    