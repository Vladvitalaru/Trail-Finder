from flask import Flask, render_template, url_for, request, redirect
from operator import itemgetter
from mywhoosh import *
import json

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('Home.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	# # global mySearcher
	if request.method == 'POST':
		query = request.form.get("search")
		url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.search(query)
  
	return render_template('results.html', results = zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty))

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

		url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.advanced_search((state_input, county_input, minlength_input, maxlength_input, 
		activities_input, surfaces_input, advancedSearch_input))

		#print("advancedResults")
		#print(state, county, minlength, maxlength, activities, surfaces, advancedSearch )

	"""links = ["https://www.traillink.com/trail/peninsula-crossing-trail/","https://www.traillink.com/trail/westside-trail/","https://www.traillink.com/trail/vera-katz-eastbank-esplanade/"]
	titles = ["Peninsula Crossing Trail","Westside Trail", "Vera Katz Eastbank Esplanade"]
	lengths = ['2.1', '3.1', '10.1']
	images = ["https://cloudfront.traillink.com/photos/peninsula-crossing-trail_23816_sc.jpg",
           "https://cloudfront.traillink.com/photos/westside-trail_107049_sc.jpg",
           "https://cloudfront.traillink.com/photos/vera-katz-eastbank-esplanade_167510_sc.jpg"]
	states = ["Oregon", "Oregon", "Oregon"]
	county = ["Multnomah", "Washington","Multnomah" ]
	descriptions = ["Peninsula Crossing Trail spans 5.1 from N. Carey Blvd. and N. Princeton St. to Columbia Slough Trail at N. Columbia Blvd.","Westside Trail spans 8.1 from Forest Park to Barrows Park.","Vera Katz Eastbank Esplanade spans 1.7 from Steel Bridge just west of NE Lloyd Blvd. to SE Caruthers St. just south of the Marquam Bridge."]
	styleID = [1,2,3]"""
	return render_template('advancedResults.html', results = zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty) ) #add review cloud and difficulty level
 
#Handle error 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
		
if __name__ == '__main__':
	#global mySearcher
	mySearcher = MyWhooshSearcher()
	#mySearcher.build_index() # Use this to build index first then uncomment
	mySearcher.existing_index()
	app.run(debug=True)
