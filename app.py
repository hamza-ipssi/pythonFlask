from flask import Flask, request, render_template, redirect, url_for
from dataModels import User, Tweet
from config import getEngine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Declaration de la classe de déclaration des modèles de BDD

engine = getEngine()
session = sessionmaker()
session.configure(bind=engine)
s = session()


# Insertion, équivalent de "INSERT INTO"
# user = User(username="Flask", email="example@example.com")
# s.add(user)
# s.commit()


@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template('newUser.html')
	if request.method == 'POST':
		return redirect(url_for('save_gazouille'))

@app.route('/gaz',methods=['GET','POST'])
def save_gazouille():
	if request.method == 'POST':
		if(len(request.form['user-name'])<= 16 and len(request.form['user-text']) <= 255 ):
			tweet = Tweet(username=request.form['user-name'], tweetText=request.form['user-text'])
			s.add(tweet)
			try:
				s.commit()
			except:
				s.rollback()
				raise
			finally:
				s.close()
			s.commit()
			print(request.form)
		else:
			return redirect(url_for('save_gazouille'))
		return redirect(url_for('timeline'))
		#return "OK"
	if request.method == 'GET':
		return render_template('formulaire.html')

@app.route('/timeline',methods=['GET'])
def timeline():
	gaz = []
	for p in s.query(Tweet).all():
		gaz.append(p)
	return render_template("timeline.html", gaz = gaz)

@app.route('/timeline/<nameUser>/',methods=['GET'])
def tweetByUser(nameUser):
	gaz = []
	for p in s.query(Tweet).filter_by(username=nameUser).all():
		gaz.append(p)
	return render_template("timeline.html", gaz = gaz)

@app.after_request
def add_header(response):
    header = response.headers
    response.cache_control.max_age = 300
    header['Access-Control-Allow-Origin'] = '*'
    return response