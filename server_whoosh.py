from flask import Flask, render_template, url_for, request
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	#return render_template('Home.html')
	return render_template('Home.html')
                        
@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mySearcher
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')
	test = data.get('test')
	titles, description = mySearcher.search(query)
	print("You searched for: " + query)
	print("Alternatively, the second box has: " + test)
 
	return render_template('results.html', query=query, results=zip(titles, description))

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
	global mySearcher
	mySearcher = MyWhooshSearcher()
	mySearcher.index()
	#title, description = mySearcher.search('hello')
	#print(title)
	app.run(debug=True)
