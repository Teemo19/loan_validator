from flask import Blueprint, render_template, redirect, url_for, request , flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

from flask_login import login_user, logout_user, login_required
from . import db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from emailsender import emailsender
from calculateCURP import CURP
auth = Blueprint('auth', __name__)

class _current_login:
    def __init__(self,email='',name='',last_name='',mother_lastname='',day='',month='',year='',gender='',entity='',curp = ''):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.mother_lastname = mother_lastname
        self.day = day
        self.month = month
        self.year = year
        self.gender = gender
        self.entity = entity
        self.curp = curp

s = URLSafeTimedSerializer('Thisisasecret!')
current_login = _current_login()
@auth.route('/checkdata',methods=['POST'])
def checkdata():
    name = request.form.get('name')
    last_name = request.form.get('lastname')
    mother_lastname = request.form.get('mother_lastname')
    fecha_de_nacimiento = request.form.get('birthday')
    day = fecha_de_nacimiento[8:10]
    month = fecha_de_nacimiento[5:7]
    year = fecha_de_nacimiento[:4]
    gender = request.form.get('gender')
    entity = request.form.get('entity')
    parameters = {'paterno': last_name,'materno':mother_lastname,'nombre':name,'dia':day,'mes':month,'anio':year,'sexo':gender,'entidad': entity}
    curp = CURP(parameters).pstCURP
    current_login.name = name
    current_login.last_name = last_name
    current_login.mother_lastname = mother_lastname
    current_login.day = day
    current_login.month = month
    current_login.year = year
    current_login.gender = gender
    current_login.entity = entity
    current_login.curp = curp
    #token = s.dumps([email,name,password], salt='email-confirm')
    #link = url_for('auth.confirm_email', token=token, _external=True)
    text = 'hi {}  your submit is being processed & you will be informed if your loan is successfully authorized or not'.format(current_login.name)
    mail = emailsender("testloan1000","Ninjavisioni7",current_login.email,"Confirm Email",text)
    mail.send_text()
    return '<h1> Email sent to {}</h1>'.format(current_login.email)

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        data = s.loads(token, salt='email-confirm', max_age=3600)
        email = data[0]
        name = data[1]
        password = data[2]
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return  redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    current_login.email=email
    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    token = s.dumps([email,name,password], salt='email-confirm')
    link = url_for('auth.confirm_email', token=token, _external=True)
    text = 'Your link is {}'.format(link)
    mail = emailsender("testloan1000","Ninjavisioni7",email,"Confirm Email",text)
    mail.send_text()
    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

    
@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

