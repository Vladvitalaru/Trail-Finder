from flask import Flask, request, render_template, redirect, url_for
from operator import itemgetter
from mywhoosh import *
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('Home.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	# # global mySearcher
	# data = request
	if request.method == 'POST':
		# query = request.form.get("search")
		# query = search.get('search')
		state = request.form.get("state")
		query = request.form.get("search")
		# state = request.form['state']
		# state = advanced.get('state')
		# county = data.get('county')
		# print(query)
		# state = request.form['state']

		print(state, query)

		# print(state)
		# state = "test"
		# print(county)
	# 	return redirect(url_for('results', input=data))
	# else:
	# 	# input = request.form["search"] 
	# results = [{'title': 'Example Trail Title', 'length': '2.1 Miles'},
    #        {'title': 'Example Trail Title2', 'length': '3.1 Miles'}]
	links = ["https://www.traillink.com/trail/peninsula-crossing-trail/","https://www.traillink.com/trail/westside-trail/","https://www.traillink.com/trail/vera-katz-eastbank-esplanade/"]
	titles = ["Peninsula Crossing Trail","Westside Trail", "Vera Katz Eastbank Esplanade"]
	lengths = ['2.1 Miles', '3.1 Miles', '10.1 Miles']
	images = ["https://cloudfront.traillink.com/photos/peninsula-crossing-trail_23816_sc.jpg",
           "https://cloudfront.traillink.com/photos/westside-trail_107049_sc.jpg",
           "https://cloudfront.traillink.com/photos/vera-katz-eastbank-esplanade_167510_sc.jpg"]
	states = ["Oregon", "Oregon", "Oregon"]
	county = ["Multnomah", "Washington","Multnomah" ]
	descriptions = ["Peninsula Crossing Trail spans 5.1 from N. Carey Blvd. and N. Princeton St. to Columbia Slough Trail at N. Columbia Blvd.","Westside Trail spans 8.1 from Forest Park to Barrows Park.","Vera Katz Eastbank Esplanade spans 1.7 from Steel Bridge just west of NE Lloyd Blvd. to SE Caruthers St. just south of the Marquam Bridge."]
	styleID = [1,2,3]
	return render_template('results.html', results = zip(links, titles, lengths, images, states, county, descriptions, styleID) )
 
 
	# 	data = request.args

	# query = data.get('searchterm')
	# test = data.get('test')
	# titles, description = mySearcher.search(query)
	# print("You searched for: " + query)
	# print("Alternatively, the second box has: " + test)
 
	# return render_template('results.html', query=query, results=zip(titles, description))
	#return "Hello world!"
	# return render_template('results.html')

#Handle error 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404



# indexer = index()
# search(indexer, 'nice')

if __name__ == '__main__':
	# global mySearcher
	# mySearcher = MyWhooshSearcher()
	# mySearcher.build_index()
	#title, description = mySearcher.search('hello')
	#print(title)
	app.run(debug=True)
