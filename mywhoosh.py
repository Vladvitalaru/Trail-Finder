
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
import os
import re
import json


class MyWhooshSearcher(object):
	"""Class to be used for indexing and searching"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()
		
		
	def search(self, queryEntered):
		"""Yet to be updated, should be updated to a general search with all the necessary fields and an advanced search as two separate methods"""
		title = list()
		state = list()
		county = list()
		with self.indexer.searcher() as search:
			query = MultifieldParser(['title', 'state', 'county', 'activities'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			results = search.search(query, limit=10)
			
			for x in results:
				title.append(x['title'])
				state.append(x['state'])
				county.append(x['county'])
			
		return title, state, county
	
	def existing_index(self):
		"""Loads an existing index at /myIndex/"""
		self.indexer = open_dir('myIndex')

	def build_index(self):
		"""Creates a new index based on the file path given containing documents"""
		corpus_path = "./files"
		schema = Schema(url=ID(stored=True), title=TEXT(stored=True), length=NUMERIC(int, decimal_places=2,stored=True, signed=False), 
			image=STORED, state=KEYWORD(stored=True,commas=True), county=KEYWORD(stored=True,commas=True), 
				description=STORED, trail_surfaces=KEYWORD(commas=True), activities=KEYWORD(commas=True), content=KEYWORD)
		indexer = create_in('myIndex', schema)
		writer = indexer.writer()
		file_names = os.listdir(corpus_path)
		#i = 0
		for name in file_names:
			full_path = os.path.join(corpus_path, name)
			if os.path.isfile(full_path): #make sure we aren't reading directories
				#open file and begin parsing
				#i += 1
				with open(full_path, 'r') as f:
					json_dict = json.loads(f.readline())
					if len(json_dict['images']) > 0:
						image_url = json_dict['images'][0]
					else:
						image_url = "https://www.traillink.com/images/tl/placeholders/No_Photo_Image_Thumbnail-trimmed.jpg"
					activity_string = ",".join(json_dict['facts']['activities'])
					review_cloud_path = "cloud.png" #temporary path based on our current default word cloud image
					len_dec = Decimal(json_dict['facts']['Length'].rstrip(" miles"))
					writer.add_document(url=json_dict['url'], title=json_dict['title'], length=len_dec,
					image=image_url, state=json_dict['facts']['States'], county=json_dict['facts']['Counties'],
					description=json_dict['description'], trail_surfaces=json_dict['facts']['Trail surfaces'],
					activities=activity_string, content=json_dict['content'])

		writer.commit()

		self.indexer = indexer

# indexer = index()
# search(indexer, 'nice')

if __name__ == '__main__':
	# global mySearcher #may want to uncomment?
	mySearcher = MyWhooshSearcher()
	#mySearcher.build_index()
	mySearcher.existing_index()
	title, state, county = mySearcher.search('gorge')
	for a,b,c in zip(title, state, county):
		print(f'{a} {b} {c}')
