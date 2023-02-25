from flask import Flask, redirect, url_for, request, jsonify, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from forms import registration_form, login_form

import json

import importlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a9d3b60f729f30d5ce93d0ce07429e2f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)
class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(30), nullable=False)
  lname = db.Column(db.String(30), nullable=False)
  username = db.Column(db.String(30), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  profilepic = db.Column(db.String(120), default = 'mustang.jpeg')
  hashed_password = db.Column(db.LargeBinary(128), nullable=False)
  scores = db.Column(db.Integer, nullable=False, default=0)
  totalscore = db.Column(db.Integer, nullable=False, default=0)
  def __repr__(self) -> str:
     return f'user: {self.username} email: {self.email}, pfp: {self.profilepic}, password: {self.password}'

@app.route("/", methods= ["GET", "POST"])
def mainpage():
  if 'username' in session:
    first_name = session.get('first_name')
    profilepic = session.get('profilepic')
    return render_template('mainpage.html', PageTitle = 'Main Page', first_name=first_name, profilepic=profilepic)
  else:
    return(render_template('mainpage.html', PageTitle = 'Main Page'))



@app.route("/processdata", methods=["POST"])
def process_data():
  data = request.get_json()
  if data["restart"]:
    # Rerun the Python script
    import pyt_back # have to re-import the script since it was imported locally
    importlib.reload(pyt_back)
    data = json.dumps(pyt_back.game_infrastructure.info_dict)
    targetcar = json.dumps(pyt_back.game_infrastructure.target_car)
  else:
    result = "Invalid request"
  return jsonify({'data': data, 'targetcar': targetcar})

@ app.route('/BAT', methods= ['GET', 'POST'])    
def price_game():
    from finding_listings import Finding_listing
    car_info = json.dumps(Finding_listing.car_info)
    return render_template('prices.html', car_info=car_info)

@ app.route('/about', methods = ['GET', 'POST'])
def aboutme():
    return render_template('aboutme.html')  

@app.route('/login', methods= ['GET', 'POST'])
def login():
  form = login_form()
  print(form.username.data)
  print(form.password.data)
  user = Player.query.filter(Player.username==form.username.data).first()
  
  if user:
    if bcrypt.checkpw(request.form['password'].encode('utf-8'), user.hashed_password):
      session['username'] = user.username
      session['score'] = user.scores
      session['first_name'] = user.fname
      session['profilepic'] = user.profilepic
      session['last_name'] = user.lname
      session['total_score'] = user.totalscore
      print(user.profilepic)
      print(user.scores)
      print(user.totalscore)
      first_name = session.get('first_name')
      last_name = session.get('last_name')
      profilepic = session.get('profilepic')
      print(first_name)
      print(last_name)
   #player = Player.query.filter(Player.username == 'Sean').first() is a sample query
    return render_template('mainpage.html', first_name = first_name, last_name=last_name, profilepic = profilepic)
  else:
    #fetch request accounting for message
    flash('Note: Login is required for Carguessr', 'danger')
  return render_template('login.html', title= 'Login!', form = form)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
  form = registration_form()
  if form.password.data != form.confirm_password.data:
    flash('Passwords do not match', 'danger')
    return redirect(url_for('create_account'))
  if Player.query.filter_by(username=form.username.data).first(): #if it finds something that's already there
    flash('Username already taken', 'danger')
    return redirect(url_for('create_account'))
  if form.validate_on_submit():
    hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
    player = Player(fname = form.fname.data, lname= form.lname.data, username=form.username.data, email=form.email.data, hashed_password=hashed_password)
    db.session.add(player)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('create_account.html', form = form)
@app.route("/specs", methods= ['GET', 'POST']) 
def spec_game():   
    from pyt_back import game_infrastructure
    data = json.dumps(game_infrastructure.info_dict)
    targetcar = json.dumps(game_infrastructure.target_car)
    print(targetcar)
    first_name = session.get('first_name')
    if 'username' not in session:
      return redirect(url_for('login'))
    else:
      print('this is the players name:' + first_name)
      player_score = session.get('score')
      player = Player.query.filter_by(username=Player.username).first()
      totalscore = player.totalscore
      correctscore = player.scores
      profilepic = session.get('profilepic')
      print(profilepic)
      print(player_score)
      return render_template("index.html", PageTitle = 'Name that Car!', data=data, targetcar=targetcar, correctscore=correctscore, totalscore=totalscore, player_score = player_score, profilepic=profilepic, first_name= first_name )
@app.route('/changescore', methods=['POST', 'GET'])
def update_totalscore():
    if request.method == 'POST':
        data = request.get_json()
        totalscore = data['totalscore']
        totalscore = int(totalscore) +1
        player = Player.query.filter_by(username=Player.username).first()
        player.totalscore = totalscore
        db.session.commit()
    elif request.method == 'GET':
        player = Player.query.filter_by(username=Player.username).first()
        totalscore = player.totalscore
    return jsonify({'new_score': totalscore})

@app.route('/changecorrectscore', methods=['POST', 'GET'])
def update_correctscore():
    if request.method == 'POST':
        data = request.get_json()
        correctscore = data['correctscore']
        correctscore = int(correctscore) +1
        player = Player.query.filter_by(username=Player.username).first()
        player.scores = correctscore
        db.session.commit()
    elif request.method == 'GET':
        player = Player.query.filter_by(username=Player.username).first()
        correctscore = player.scores
    return jsonify({'correct_score': correctscore})

@app.route('/logout', methods=['GET','POST'])
def logout():
  session.pop('username')
  session.pop('first_name')
  session.pop('last_name')
  session.pop('profilepic')

  return redirect(url_for('mainpage'))



if __name__ == '__main__':
    app.run(debug=True)


