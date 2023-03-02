
import decimal
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.query import NumericRange
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
import os
import json
import matplotlib.pyplot as plotter
from wordcloud import WordCloud
from wordcloud import STOPWORDS

class MyWhooshSearcher(object):
	"""Class to be used for indexing and searching"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()

	def search(self, queryEntered):
		"""General search with all the necessary fields"""
		with open('traillinkPR.txt', 'r') as f:
			traillinkPR = json.loads(f.read())
			url, title, length, image, state, county, description, activity, surfaces, cloud, difficulty = ([] for _ in range(11))
			with self.indexer.searcher() as search:
				query = MultifieldParser(['length', 'title', 'state', 'county', 'activities', 'content'], schema=self.indexer.schema)
				query = query.parse(queryEntered)
				results = search.search(query, limit=None)
				list_to_sort = []
				for x in results:
					try:
						url_score = x.score + traillinkPR(x['url'])
					except:
						url_score = x.score
					list_to_sort.append((x, url_score))
					list_to_sort.sort(key= lambda x: x[1], reverse=True)
				for x, x.score in list_to_sort:
					if x['url'].endswith('trail-detail-reviews'): pass #will want to remove once crawler is fixed
					else:
						url.append(x['url'])
						title.append(x['title'])
						length.append(x['length'])
						image.append(x['image'])
						state.append(x['state'])
						county.append(x['county'])
						description.append(x['description'])
						activity.append(x['activities'].replace(',' , ', '))
						try: surfaces.append(x['trail_surfaces'])
						except: surfaces.append(queryEntered)
						cloud.append(x['cloud_path'])
						len_for_diff = float(x['length'])
						if len_for_diff < 8: difficulty.append('Easy')
						elif len_for_diff < 15: difficulty.append('Medium')
						else: difficulty.append('Hard')
			styleID = [i for i in range(1,len(url)+1)]
			return url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty

	def advanced_search(self, queryEntered: tuple): #queryEntered = (state, county, minLength, maxLength, activities, surfaces, advSearch)
		"""Advanced Search where query goes to specific fields, works even if all fields are not present"""
		url, title, length, image, state, county, description, activity, surfaces, cloud, difficulty = ([] for _ in range(11))
		with open('traillinkPR.txt', 'r') as f:
			traillinkPR = json.loads(f.read())
			with self.indexer.searcher() as search: #minLength:maxLength
				state_query = QueryParser('state', schema=self.indexer.schema)
				state_query = state_query.parse(queryEntered[0])
				county_query = QueryParser('county', schema=self.indexer.schema)
				county_query = county_query.parse(queryEntered[1])

				if queryEntered[2] and queryEntered[3]: #min and max entered
					length_query = NumericRange('length', queryEntered[2], queryEntered[3])
				elif not queryEntered[2] and queryEntered[3]: #only max entered
					length_query = NumericRange('length', 0, queryEntered[3])
				elif queryEntered[2] and not queryEntered[3]: #only min entered
					length_query = NumericRange('length', queryEntered[2], 9999)
				elif not queryEntered[2] and not queryEntered[3]: #neither entered
					length_query = NumericRange('length', 0, 9999)

				activity_query = QueryParser('activities', schema=self.indexer.schema)
				activity_query = activity_query.parse(queryEntered[4])
				surface_query = QueryParser('trail_surfaces', schema=self.indexer.schema)
				surface_query = surface_query.parse(queryEntered[5])
				general_query = MultifieldParser(['titles','content'], schema=self.indexer.schema)
				general_query = general_query.parse(queryEntered[6])

				results = search.search(length_query, limit=None)
				if county_query:
					county_results = search.search(county_query, limit=None)
					results.filter(county_results)
				if activity_query:
					activity_results = search.search(activity_query, limit=None)
					results.filter(activity_results)
				if surface_query:
					surface_results = search.search(surface_query, limit=None)
					results.filter(surface_results)
				if state_query:
					state_results = search.search(state_query, limit=None)
					results.filter(state_results)
				if general_query:
					general_results = search.search(general_query, limit=None)
					results.filter(general_results)

				list_to_sort = []
				for x in results:
					try:
						url_score = x.score + traillinkPR(x['url'])
					except:
						url_score = x.score
					list_to_sort.append((x, url_score))
					list_to_sort.sort(key= lambda x: x[1], reverse=True)
				for x, x.score in list_to_sort:
					if x['url'].endswith('trail-detail-reviews'): pass #will want to remove once crawler is fixed
					else:
						url.append(x['url'])
						title.append(x['title'])
						length.append(x['length'])
						image.append(x['image'])
						state.append(x['state'])
						county.append(x['county'])
						description.append(x['description'])
						activity.append(x['activities'].replace(',' , ', '))
						try: surfaces.append(x['trail_surfaces'])
						except: surfaces.append(queryEntered)
						cloud.append(x['cloud_path'])
						len_for_diff = float(x['length'])
						if len_for_diff < 5: difficulty.append('Easy')
						elif len_for_diff < 12: difficulty.append('Medium')
						else: difficulty.append('Hard')
						#matching = []
						#for term in x.matched_terms():
							#matching.append(str(term[1]).lstrip('b'))
						#matched.append(','.join(matching))
			styleID = [i for i in range(1,len(url)+1)]
			return url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty

	def existing_index(self):
		"""Loads an existing index at /myIndex/"""
		self.indexer = open_dir('myIndex')

	def build_index(self):
		"""Creates a new index based on the file path given containing documents"""
		corpus_path = "./files"
		schema = Schema(url=STORED, title=TEXT(stored=True), length=NUMERIC(int, decimal_places=2,stored=True, signed=False), 
			image=STORED, state=KEYWORD(stored=True,commas=True), county=KEYWORD(stored=True,commas=True), 
			description=STORED, trail_surfaces=KEYWORD(commas=True,stored=True), activities=KEYWORD(commas=True,stored=True), content=KEYWORD, cloud_path=STORED)
		if not os.path.exists('myIndex'):
			os.mkdir('myIndex')
		indexer = create_in('myIndex', schema)
		writer = indexer.writer()
		file_names = os.listdir(corpus_path)
		titles_for_keyword = []
		for name in file_names:
			full_path = os.path.join(corpus_path, name)
			if os.path.isfile(full_path): #make sure we aren't reading directories
				with open(full_path, 'r') as f: #open file and begin parsing
					json_dict = json.loads(f.readline())
					if 'oregonhikers' in json_dict['url']:
						desc = json_dict['description'].split('.')
						desc = desc[0] + '.'
					else:
						desc = json_dict['description']
					if len(json_dict['images']) > 0: image_url = json_dict['images'][0]
					else: image_url = "https://www.traillink.com/images/tl/placeholders/No_Photo_Image_Thumbnail-trimmed.jpg"
					try:
						activity_string = ",".join(json_dict['facts']['activities'])
					except:
						activity_string = ''
					review = "".join(json_dict['reviews'])
					review.strip()
					review_cloud_path = name.rstrip('.txt') + '.png'
					if os.path.exists('./static/images/cloud/' + review_cloud_path): pass
					elif len(review) > 0:
						review = "".join(json_dict['reviews'])
						stopwords = set(STOPWORDS)
						stopwords.add('trail')
						word_cloud = WordCloud(width = 800, height = 600,
						background_color='white', stopwords = stopwords,
						min_font_size = 10).generate(review)
						plotter.figure(figsize=(8,6), facecolor = None)
						plotter.imshow(word_cloud)
						plotter.axis('off')
						plotter.tight_layout(pad=0)
						plotter.savefig('./static/images/cloud/' + review_cloud_path)
						plotter.close()
					elif 'oregonhikers' in json_dict['url']:
						stopwords = set(STOPWORDS)
						stopwords.add('trail')
						word_cloud = WordCloud(width = 800, height = 600,
						background_color='white', stopwords = stopwords,
						min_font_size = 10).generate(json_dict['description'])
						plotter.figure(figsize=(8,6), facecolor = None)
						plotter.imshow(word_cloud)
						plotter.axis('off')
						plotter.tight_layout(pad=0)
						plotter.savefig('./static/images/cloud/' + review_cloud_path)
						plotter.close()
					else: review_cloud_path = "cloud.png" #path based on our current default word cloud image
					len_dec = Decimal(json_dict['facts']['Length'].rstrip(" miles").lstrip('~'))
					writer.add_document(url=json_dict['url'], title=json_dict['title'], length=len_dec,
						image=image_url, state=json_dict['facts']['States'], county=json_dict['facts']['Counties'],
						description=desc, trail_surfaces=json_dict['facts']['Trail surfaces'],
						activities=activity_string, content=json_dict['content'], cloud_path = review_cloud_path)
					titles_for_keyword.append(json_dict['title'])
		writer.commit()
		self.indexer = indexer
		with open('./static/titles.txt', 'w') as f:
			for line in titles_for_keyword:
				f.write(line + "\n")

if __name__ == '__main__':
	mySearcher = MyWhooshSearcher()
	mySearcher.build_index()
	#mySearcher.existing_index()
	"""url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty = mySearcher.advanced_search(('Maine', 'Aroostook', 0, 200, 'ATV', 'Gravel', 'moose'))
	for a,b,c,d,e,f,g,h,i,j,k,l in zip(url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty):
		print(f'{a} {b} {c} {d} {e} {f} {g} {h} {i} {j} {k} {l}')"""
