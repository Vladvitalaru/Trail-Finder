from flask import Flask, render_template, url_for, request, redirect
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from operator import itemgetter

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('Home.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	# # global mySearcher
	# data = request
	if request.method == 'POST':
		data = request.form
	
	# query = data.get('search')
	# 	data = request.form["search"]
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

class MyWhooshSearcher(object):
	"""docstring for MyWhooshSearcher"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()
		
		
	def search(self, queryEntered):
		title = list()
		description = list()
		with self.indexer.searcher() as search:
			query = MultifieldParser(['title', 'description'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			results = search.search(query, limit=None)
			
			for x in results:
				title.append(x['title'])
				description.append(x['description'])
			
		return title, description

	def index(self):
		schema = Schema(id=ID(stored=True), title=TEXT(stored=True), description=TEXT(stored=True))
		indexer = create_in('myIndex', schema)
		writer = indexer.writer()

		writer.add_document(id=u'1', title=u'hello there', description=u'cs hello, how are you')
		writer.add_document(id=u'2', title=u'hello bye', description=u'nice to meetcha')
		writer.commit()

		self.indexer = indexer

# indexer = index()
# search(indexer, 'nice')

if __name__ == '__main__':
	# global mySearcher
	# mySearcher = MyWhooshSearcher()
	# mySearcher.index()
	#title, description = mySearcher.search('hello')
	#print(title)
	app.run(debug=True)
