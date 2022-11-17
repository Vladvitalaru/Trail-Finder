from flask import Flask, render_template, url_for, request, redirect
from operator import itemgetter
from mywhoosh import *
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
import random
import os
import re
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
		url, title, length, image, state, county, description, styleID = mySearcher.search(query)
	return render_template('results.html', results = zip(url, title, length, image, state, county, description, styleID))

@app.route('/advancedResults/', methods=['GET', 'POST'])
def advancedResults():
	# # global mySearcher
	if request.method == 'POST':
		state = request.form.get("state")
		county = request.form.get("county")
		minlength = request.form.get("minLength")
		maxlength = request.form.get("maxLength")
		activities = request.form.get("activities")
		surfaces = request.form.get("surfaces")
		advancedSearch = request.form.get("advancedSearch")

		print("advancedResults")
		print(state, county, minlength, maxlength, activities, surfaces, advancedSearch )

	links = ["https://www.traillink.com/trail/peninsula-crossing-trail/","https://www.traillink.com/trail/westside-trail/","https://www.traillink.com/trail/vera-katz-eastbank-esplanade/"]
	titles = ["Peninsula Crossing Trail","Westside Trail", "Vera Katz Eastbank Esplanade"]
	lengths = ['2.1', '3.1', '10.1']
	images = ["https://cloudfront.traillink.com/photos/peninsula-crossing-trail_23816_sc.jpg",
           "https://cloudfront.traillink.com/photos/westside-trail_107049_sc.jpg",
           "https://cloudfront.traillink.com/photos/vera-katz-eastbank-esplanade_167510_sc.jpg"]
	states = ["Oregon", "Oregon", "Oregon"]
	county = ["Multnomah", "Washington","Multnomah" ]
	descriptions = ["Peninsula Crossing Trail spans 5.1 from N. Carey Blvd. and N. Princeton St. to Columbia Slough Trail at N. Columbia Blvd.","Westside Trail spans 8.1 from Forest Park to Barrows Park.","Vera Katz Eastbank Esplanade spans 1.7 from Steel Bridge just west of NE Lloyd Blvd. to SE Caruthers St. just south of the Marquam Bridge."]
	styleID = [1,2,3]
	return render_template('advancedResults.html', results = zip(links, titles, lengths, images, states, county, descriptions, styleID) )
 
#Handle error 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

class MyWhooshSearcher(object):
	"""Class to be used for indexing and searching"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()

	def search(self, queryEntered):
		"""Yet to be updated, should be updated to a general search with all the necessary fields and an advanced search as two separate methods"""
		url, title, length, image, state, county, description, styleID = ([] for _ in range(8))
		for _ in range(0, 10): styleID.append(random.randint(1, 4)) # generate random styleID list for testing
		with self.indexer.searcher() as search:
			query = MultifieldParser(['url', 'length', 'title', 'image', 'state', 'county', 'description', 'activities'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			results = search.search(query, limit=10)
			for x in results:
				if x['url'].endswith('trail-detail-reviews'): pass
				else:
					url.append(x['url'])
					title.append(x['title'])
					length.append(str(x['length'])+' Miles')
					image.append(x['image'])
					state.append(x['state'])
					county.append(x['county'])
					description.append(x['description'])
		return url, title, length, image, state, county, description, styleID

	def existing_index(self):
		"""Loads an existing index at /myIndex/"""
		self.indexer = open_dir('myIndex')

	def build_index(self):
		"""Creates a new index based on the file path given containing documents"""
		corpus_path = "./files"
		schema = Schema(url=ID(stored=True), title=TEXT(stored=True), length=NUMERIC(int, decimal_places=2,stored=True, signed=False), 
			image=TEXT(stored=True), state=KEYWORD(stored=True,commas=True), county=KEYWORD(stored=True,commas=True), 
			description=TEXT(stored=True), trail_surfaces=KEYWORD(commas=True), activities=KEYWORD(commas=True), content=KEYWORD)
		indexer = create_in('myIndex', schema)
		writer = indexer.writer()
		file_names = os.listdir(corpus_path)
		for name in file_names:
			full_path = os.path.join(corpus_path, name)
			if os.path.isfile(full_path): #make sure we aren't reading directories
				with open(full_path, 'r') as f: #open file and begin parsing
					json_dict = json.loads(f.readline())
					if len(json_dict['images']) > 0: image_url = json_dict['images'][0]
					else: image_url = "https://www.traillink.com/images/tl/placeholders/No_Photo_Image_Thumbnail-trimmed.jpg"
					activity_string = ",".join(json_dict['facts']['activities'])
					review_cloud_path = "cloud.png" #temporary path based on our current default word cloud image
					len_dec = Decimal(json_dict['facts']['Length'].rstrip(" miles"))
					writer.add_document(url=json_dict['url'], title=json_dict['title'], length=len_dec,
						image=image_url, state=json_dict['facts']['States'], county=json_dict['facts']['Counties'],
						description=json_dict['description'], trail_surfaces=json_dict['facts']['Trail surfaces'],
						activities=activity_string, content=json_dict['content'])
		writer.commit()
		self.indexer = indexer
		
if __name__ == '__main__':
	global mySearcher
	mySearcher = MyWhooshSearcher()
	#mySearcher.build_index() # Use this to build index first then uncomment
	mySearcher.existing_index()
	app.run(debug=True)
