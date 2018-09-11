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

#Homepage
@app.route("/", methods=["POST", "GET"])
def index():
	return render_template("index.html")


@app.route("/books", methods=["POST", "GET"])
def books():
	book_search = request.form.get("books")
	search_result = db.execute("SELECT * FROM books WHERE title = :books OR isbn = :books OR author = :books",
		{"books": book_search}).fetchall()
	print (search_result)
	if len(search_result)<1:
		return render_template("error.html", message="There is no such book")
	else:	
		return render_template("books.html")

#Login page
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method=="GET":
		return render_template("login.html")
	
	elif request.method=="POST":
		username = request.form.get("username")
		password = request.form.get("password")
		hashed_password = encrypt_string(password)
		login_data = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
			{"username": username, "password": hashed_password}).fetchall()
		if len(login_data)<1:
			return render_template("error.html", message="Wrong user or password, try again")
		else:
			return render_template("success.html", message="You are logged in")

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
		signup_data = db.execute("SELECT * FROM users WHERE username = :username",
			{"username": username}).fetchall()
		if len(signup_data)>0:
			return render_template("error.html", message="Username already taken, choose a new one")
		else:
			db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
			{"name": name, "username": username, "password": hashed_password})		
		db.commit()
		return render_template("success.html", message="You created a new account")

#User page


	
