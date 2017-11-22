from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/search")
def search():
	last_name = request.args.get('firstname')
	first_name = request.args.get('lastname')
	email = request.args.get('email')
	phone = request.args.get('phone')
	gender = request.args.get('gender')
	specialty = request.args.get('specialty')
	address = request.args.get('address')

	# query database and try to match

	query = "SELECT * FROM dentists"

	results = []

	return jsonify(results)


@app.route("/view/<int:id>")
def view(id):

	# query dentists database by id

	dentist_profile = {'id': id}

	return jsonify(dentist_profile)

# User routes

#	/						homepage, with a search box and result display

# API routes
#	GET		/search			search the database with dentist params
#	GET		/view			given dentist ID, load more info