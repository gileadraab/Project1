import os
import hashlib

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


@app.route("/")
def index():
	return render_template("index.html")

#Login page
@app.route("/login")
def login():
	return render_template("login.html")

#Create account page
@app.route("/create_account", methods=["POST", "GET"])
def create_account():
	"Create an Account"
	if request.method=="GET":
		return render_template("create.html")

	elif request.method=="POST":
		name = request.form.get("name")
		username = request.form.get("username")
		password = request.form.get("password")
		hashed_password = encrypt_string(password)
		db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
			{"name": name, "username": username, "password": hashed_password})		
		db.commit()
		return "Succes!"

#User page
@app.route("/user", methods=["POST"])
def user():
	username = request.form.get("username")
	password = request.form.get("password")
	db.execute("SELECT * FROM users WHERE username = :username",{"username":username})
	return "under construction..."

	
