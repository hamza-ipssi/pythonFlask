from flask import Flask, request, render_template, redirect, url_for
import csv
# import mysql.connector
# import sshtunnel
import setting
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Boolean, String, Integer, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


# Declaration de la classe de déclaration des modèles de BDD
Base = declarative_base()

engine = create_engine(setting.CONST_BD)

session = sessionmaker()
session.configure(bind=engine)
s = session()




class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(16), unique=True, nullable=False)

class Tweet(Base):
    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=False, nullable=False)
    tweetText = Column(String(255), unique=False, nullable=False)

Base.metadata.create_all(engine)

print("---- print ----")
for p in s.query(User).all():
    print(p)

# Insertion, équivalent de "INSERT INTO"
# user = User(username="Flask", email="example@example.com")
# s.add(user)
# s.commit()


@app.route('/', methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template('newUser.html')
	if request.method == 'POST':
		return redirect(url_for('save_gazouille'))

@app.route('/gaz', methods=['GET','POST'])
def save_gazouille():
	if request.method == 'POST':
		if(len(request.form['user-name'])> 16 or request.form['user-text'] >255 ):
			tweet = Tweet(username=request.form['user-name'], tweetText=request.form['user-text'])
			s.add(tweet)
			s.commit()
			print(request.form)
			# dump_to_csv(request.form)
		else:
			return redirect(url_for('save_gazouille'))
		return redirect(url_for('timeline'))
		#return "OK"
	if request.method == 'GET':
		return render_template('formulaire.html')

@app.route('/timeline', methods=['GET'])
def timeline():
	gaz = []
	for p in s.query(Tweet).all():
		gaz.append(p)
	return render_template("timeline.html", gaz = gaz)

def parse_from_csv():
	gaz = []
	with open('./gazouilles.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			gaz.append({"user":row[0], "text":row[1]})
	return gaz

def dump_to_csv(d):
	donnees = [d["user-name"],d["user-text"] ]
	with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(donnees)