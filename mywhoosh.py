
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.query import NumericRange
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

	def search(self, queryEntered, pageNum):
		"""Yet to be updated, should be updated to a general search with all the necessary fields and an advanced search as two separate methods"""
		url, title, length, image, state, county, description = ([] for _ in range(7))
		styleID = [i for i in range(1,11)]
		with self.indexer.searcher() as search:
			query = MultifieldParser([ 'length', 'title', 'state', 'county', 'activities', 'content'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			page = search.search_page(query, pageNum, pagelen=20)
			for x in page.results:
				if x['url'].endswith('trail-detail-reviews'): pass #will want to remove once crawler is fixed
				else:
					url.append(x['url'])
					title.append(x['title'])
					length.append(x['length'])
					image.append(x['image'])
					state.append(x['state'])
					county.append(x['county'])
					description.append(x['description'])
		return url, title, length, image, state, county, description, styleID

	def advanced_search(self, queryEntered: tuple): #queryEntered = (state, county, minLength, maxLength, activities, surfaces, advSearch)
		url, title, length, image, state, county, description = ([] for _ in range(7))
		styleID = [i for i in range(1,11)]
		matched=list()

		with self.indexer.searcher() as search: #minLength:maxLength
			state_query = QueryParser('state', schema=self.indexer.schema)
			state_query = state_query.parse(queryEntered[0])
			county_query = QueryParser('county', schema=self.indexer.schema)
			county_query = county_query.parse(queryEntered[1])
			length_query = NumericRange('length', queryEntered[2], queryEntered[3])
			#length_query = QueryParser('length', schema=self.indexer.schema)
			#length_query = length_query.parse(queryEntered[2] + ':' + queryEntered[3])
			activity_query = QueryParser('activities', schema=self.indexer.schema)
			activity_query = activity_query.parse(queryEntered[4])
			surface_query = QueryParser('trail_surfaces', schema=self.indexer.schema)
			surface_query = surface_query.parse(queryEntered[5])
			general_query = MultifieldParser(['titles','content'], schema=self.indexer.schema)
			general_query = general_query.parse(queryEntered[6])


			results = search.search(state_query, limit=None)
			county_results = search.search(county_query, limit=None)
			length_results = search.search(length_query, limit=None)
			activity_results = search.search(activity_query, limit=None)
			surface_results = search.search(surface_query, limit=None)
			general_results = search.search(general_query, limit=None)
			results.upgrade_and_extend(county_results)
			results.upgrade_and_extend(length_results)
			results.upgrade_and_extend(activity_results)
			results.upgrade_and_extend(surface_results)
			results.upgrade_and_extend(general_results)

			for x in results:
				if x['url'].endswith('trail-detail-reviews'): pass #will want to remove once crawler is fixed
				else:
					url.append(x['url'])
					title.append(x['title'])
					length.append(x['length'])
					image.append(x['image'])
					state.append(x['state'])
					county.append(x['county'])
					description.append(x['description'])
					#matching = []
					#for term in x.matched_terms():
						#matching.append(str(term[1]).lstrip('b'))
					#matched.append(','.join(matching))
		return url, title, length, image, state, county, description, styleID


	def existing_index(self):
		"""Loads an existing index at /myIndex/"""
		self.indexer = open_dir('myIndex')

	def build_index(self):
		"""Creates a new index based on the file path given containing documents"""
		corpus_path = "./files"
		schema = Schema(url=STORED, title=TEXT(stored=True), length=NUMERIC(int, decimal_places=2,stored=True, signed=False), 
			image=STORED, state=KEYWORD(stored=True,commas=True), county=KEYWORD(stored=True,commas=True), 
			description=STORED, trail_surfaces=KEYWORD(commas=True), activities=KEYWORD(commas=True), content=KEYWORD, cloud_path=STORED)
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
						activities=activity_string, content=json_dict['content'], cloud_path = review_cloud_path)
		writer.commit()
		self.indexer = indexer

if __name__ == '__main__':
	#global mySearcher #may want to uncomment?
	mySearcher = MyWhooshSearcher()
	#mySearcher.build_index()
	mySearcher.existing_index()
	url, title, length, image, state, county, description, styleID = mySearcher.advanced_search(('Maine', 'Aroostook', 0, 200, 'ATV', 'Gravel', 'moose'))
	for a,b,c,d,e,f,g,h in zip(url, title, length, image, state, county, description, styleID):
		print(f'{a} {b} {c} {d} {e} {f} {g} {h}')
