from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #os.getenv('DATABASE_URL', None)
app.config['SECRET_KEY'] = 'meow' #os.getenv('WTF_KEY', None)
db = SQLAlchemy(app)
Bootstrap(app)

class SignUpForm(Form):
    name = StringField('name', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Valid email required.'), Length(min=5, max=50)])
    zipcode = StringField('zipcode', validators=[InputRequired(), Length(min=5, max=5)])

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignUpForm()
    if form.validate_on_submit():
        newUser = UserInfo(name = form.name.data, email = form.email.data, zipcode = form.zipcode.data)
        #return '<h1>' + form.name.data + '\n' + form.email.data + '\n' + form.zipcode.data
    return render_template('index.html', form=form)

if __name__=="__main__":
    app.run(debug=True)
    