from flask import Flask, render_template, url_for, request, redirect
from flask_paginate import Pagination, get_page_args
from operator import itemgetter
from mywhoosh import *
import json

results, url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = ([] for _ in range(13))

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('Home.html')

def get_results(offset=0, per_page=10):
    return results[offset: offset + per_page]

@app.route('/results/', methods=['GET', 'POST'])
def results():
	# # global mySearcher
	if request.method == 'POST':
		query = request.form.get("search")
		global url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty
		url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.search(query)
	global results
	results = list(zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty))
	total = len(styleID)
	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	pagination_pages = get_results(offset=offset, per_page=per_page)
	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
	return render_template('results.html', results=pagination_pages, page=page, per_page=per_page, pagination=pagination)

@app.route('/advancedResults/', methods=['GET', 'POST'])
def advancedResults():
	# # global mySearcher
	if request.method == 'POST':
		state_input = request.form.get("state")
		county_input = request.form.get("county")
		minlength_input = request.form.get("minLength")
		maxlength_input = request.form.get("maxLength")
		activities_input = request.form.get("activities")
		surfaces_input = request.form.get("surfaces")
		advancedSearch_input = request.form.get("advancedSearch")
		global url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty
		url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.advanced_search((state_input, county_input, minlength_input, maxlength_input, 
			activities_input, surfaces_input, advancedSearch_input))
	global results
	results = list(zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty))
	total = len(styleID)
	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	pagination_pages = get_results(offset=offset, per_page=per_page)
	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
	return render_template('results.html', results=pagination_pages, page=page, per_page=per_page, pagination=pagination) #add review cloud and difficulty level
 
#Handle error 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
		
if __name__ == '__main__':
	#global mySearcher
	mySearcher = MyWhooshSearcher()
	# mySearcher.build_index() # Use this to build index first then uncomment
	mySearcher.existing_index()
	app.run(debug=True, host='0.0.0.0', port=int("5000"))
