from flask import Flask, render_template, url_for, request, redirect
from flask_paginate import Pagination, get_page_args
from operator import itemgetter
from mywhoosh import *
import json

results, url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = ([] for _ in range(13))

application = Flask(__name__)
@application.route('/', methods=['GET', 'POST'])
def index():
	return render_template('Home.html')

def get_results(offset=0, per_page=10):
    return results[offset: offset + per_page]

@application.route('/results/', methods=['GET', 'POST'])
def results():
	# # global mySearcher
	if request.method == 'POST':
		query = request.form.get("search")
		global url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty
		url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.search(query)
  
	global results
	results = list(zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty))
	total = len(styleID)
	query = request.form.get("search")
	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	pagination_pages = get_results(offset=offset, per_page=per_page)
	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4', outer_window=0, inner_window=2)
	return render_template('results.html', results=pagination_pages, page=page, per_page=per_page, pagination=pagination, query=query)

 
#Handle error 404
@application.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
		
if __name__ == '__main__':
	mySearcher = MyWhooshSearcher()
	#mySearcher.build_cloud()
	#mySearcher.build_index() # Use this to build index first then uncomment
	mySearcher.existing_index()
	application.run(debug=True, host='0.0.0.0', port=int("5000"))
