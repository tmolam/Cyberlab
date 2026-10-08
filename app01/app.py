from flask import Flask, request
import pymysql
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def get_db():
	return pymysql.connect(
		host=os.getenv("DB_HOST"),
		port=3306,
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASSWORD"),
		database=os.getenv("DB_NAME"),
	)

@app.route("/")
def home():
	return """
	"<h1>Cyberlab App01</h1>
	<p>Our application is running!</p>"
	<p><a href="/users">View users</a></p>
	"""

@app.route("/users")
def users():
	conn = get_db()
	cursor = conn.cursor()

	cursor.execute("SELECT id, username, email FROM users")
	rows = cursor.fetchall()

	cursor.close()
	conn.close()

	output = "<h1>Users</h1><ul>"

	for user in rows:
		output += f"<li>{user[0]} - {user[1]} - {user[2]}</li>"

	output += "</ul>"
	return output

@app.route("/db-test")
def db_test():
	try:
		conn = get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT 1")
		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return f"<h1>Database works!</h1><p>Result : {result[0]}</p>"
	except Exception as e:
		return f"<h1>Database connection failed</h1><p>{e}</p>"

@app.route("/user")
def user():
	user_id = request.args.get("id")

	conn = get_db()
	cursor = conn.cursor()

	# Intentionally vulnerable - lab exercise only
	query = "SELECT id, username, email FROM users WHERE id = " + user_id

	print(f"Incoming ID: {user_id}")
	print(f"SQL query: {query}")

	cursor.execute(query)

	row = cursor.fetchone()

	cursor.close()
	conn.close()

	if row:
		return f"<h1>User</h1><p>ID: {row[0]}</p><p>Username: {row[1]}</p><p>Email: {row[2]}</p>"

	return "<h1>User not found</h1>"

@app.route("/safe-user")
def safe_user():
	user_id = request.args.get("id")

	conn = get_db()
	cursor = conn.cursor()

	query = "SELECT id, username, email FROM users WHERE id = %s"
	cursor.execute(query, (user_id,))

	row = cursor.fetchone()

	cursor.close()
	conn.close()

	if row:
		return f"<h1>User</h1><p>ID: {row[0]}</p><p>Username: {row[1]}</p><p>Email: {row[2]}</p>"

	return "<h1>User not found</h1>"

@app.route("/login")
def login():
	username = request.args.get("username")
	password = request.args.get("password")

	logging.info(f"Login attempt for username: {username}")
	if username and ("' OR " in username.upper() or " OR 1=1" in username.upper()):
		logging.warning(f"Possible SQL injection attempt: {username}")
	conn = get_db()
	cursor = conn.cursor()

	# Intentionally vulnerable lab exercise
	query = "SELECT id, username FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
	cursor.execute(query)

	row = cursor.fetchone()

	cursor.close()
	conn.close()

	if row:
		logging.info(f"Succesful login for username: {username}")
		return f"<h1>Login successful</h1><p>Welcome, {row[1]}!</p>"

	source_ip = request.headers.get("X-Real-IP", request.remote_addr)
	logging.warning(f"Failed login for username: {username} from {source_ip}")
	return "<h1>Login failed</h1>"

@app.route("/safe-login")
def safe_login():
	username = request.args.get("username")
	password = request.args.get("password")

	conn = get_db()
	cursor = conn.cursor()

	query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
	cursor.execute(query, (username, password))

	row = cursor.fetchone()

	cursor.close()
	conn.close()

	if row:
		return f"<h1>Login succesful</h1><p>Welcome, {row[1]}!</p>"

	return "<h1>Login failed</h1>"

app.run(host="0.0.0.0", port=5000)
