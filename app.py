from flask import Flask, jsonify, request, g, url_for
import sqlite3
import os

DATABASE = os.path.dirname(os.path.realpath(__file__)) + '/final.db'

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route("/search")
def search():
	full_name = request.args.get('name')
	last_name = request.args.get('last')
	first_name = request.args.get('first')
	gender = request.args.get('gender')
	specialty = request.args.get('specialty')
	city = request.args.get('city')
	address = request.args.get('address')
	day = request.args.get('day')
	time = request.args.get('time')

	# query database and try to match

	# 1=1 is only used to introduce the WHERE
	query = "SELECT id, first, last, address, city, specialty FROM dentists WHERE 1=1"
	results = []

	# basic search includes name and city only
	if city is not None:
		query = query + " AND UPPER(city) LIKE UPPER('%" + city + "%')"

	if full_name is not None:
		sub_names = full_name.split()
		for s in sub_names:
			query = query + " AND (UPPER(first) LIKE UPPER('%" + s + "%') OR UPPER(last) LIKE UPPER('%" + s + "%'))"
	else:
		# advanced search only

		if last_name is not None:
			query = query + " AND UPPER(last) LIKE UPPER('%" + last_name + "%')"
		
		if first_name is not None:
			query = query + " AND UPPER(first) LIKE UPPER('%" + first_name + "%')"

		if address is not None:
			query = query + " AND UPPER(address) LIKE UPPER('%" + address + "%')"
		
		if gender is not None:
			query = query + " AND gender='" + gender + "'"
		
		if specialty is not None:
			query = query + " AND specialty='" + specialty + "'"
		
		if time is not None:
			query = query + " AND (1=0"
			days = ['mon', 'tue', 'wed', 'thu', 'fri'] if (day is None) else [day]
			for d in days:
				query = query + " OR (" + d + "1 <= " + time + " AND " + d + "2 >" + time + ")"
			query = query + ")"
		elif day is not None:
			query = query + " AND " + day + "1 IS NOT NULL"
	

	with sqlite3.connect(DATABASE) as con:
		cur = con.cursor()
		cur.execute(query)

		results = cur.fetchall();
		cur.close()

    # JSONify
	fields = ['id', 'first_name', 'last_name', 'address', 'city', 'specialty']
	clean_results = []
	for r in results:
		clean_results.append(dict(zip(fields, r)))

	return jsonify(clean_results)


@app.route("/view/<id>")
def view(id):

	# query dentists database by id

	# don't forget to pass the image as well, kthxbye

	fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'address', 'city', 'phone', 'specialty', 'mon1', 'mon2', 'tue1', 'tue2', 'wed1', 'wed2', 'thu1', 'thu2', 'fri1', 'fri2']

	query = "SELECT * FROM dentists WHERE id=" + id 
	print(query)
	results = []

	with sqlite3.connect(DATABASE) as con:
		cur = con.cursor()
		cur.execute(query)

		results = cur.fetchall();

		# only take 1st entry
		results = results[0] if len(results) > 0 else None

		dentist_profile = dict(zip(fields, results)) if (results is not None) else None
		
		cur.close()


	return jsonify(dentist_profile)

# User routes

#	/						homepage, with a search box and result display

# API routes
#	GET		/search			search the database with dentist params
#	GET		/view			given dentist ID, load more info