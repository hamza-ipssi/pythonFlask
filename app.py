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



# sshtunnel.SSH_TIMEOUT = 5.0
# sshtunnel.TUNNEL_TIMEOUT = 5.0

# with sshtunnel.SSHTunnelForwarder(
#     ('ssh.pythonanywhere.com'),
#     ssh_username=setting.CONST_MYUSERNAME_PA, ssh_password=setting.CONST_MYPASSWORD_PA,
#     remote_bind_address=('hIpssi.mysql.pythonanywhere-services.com', 3306)
# ) as tunnel:
#     connection = mysql.connector.connect(
#         user=setting.CONST_MYUSERNAME_BD, password=setting.CONST_MYPASSWORD_BD,
#         host='127.0.0.1', port=tunnel.local_bind_port,
#         database='hIpssi$HRDatabase',
#     )

# Declaration de la classe de déclaration des modèles de BDD
Base = declarative_base()

engine = create_engine(setting.CONST_BD)

session = sessionmaker()
session.configure(bind=engine)
s = session()



# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + setting.CONST_MYUSERNAME_BD + ":" + setting.CONST_MYPASSWORD_BD +"@hIpssi.mysql.pythonanywhere-services.com/hIpssi$HRDatabase"
# db = SQLAlchemy(app)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(16), unique=True, nullable=False)

Base.metadata.create_all(engine)

print("---- print ----")
for p in s.query(User).all():
    print(p)

# Insertion, équivalent de "INSERT INTO"
user = User(username="Flask", email="example@example.com")
s.add(user)
s.commit()


@app.route('/', methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template('newUser.html')
	if request.method == 'POST':
		return redirect(url_for('save_gazouille'))

@app.route('/gaz', methods=['GET','POST'])
def save_gazouille():
	if request.method == 'POST':
		print(request.form)
		dump_to_csv(request.form)
		return redirect(url_for('timeline'))
		#return "OK"
	if request.method == 'GET':
		return render_template('formulaire.html')

@app.route('/timeline', methods=['GET'])
def timeline():
	gaz = parse_from_csv()
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