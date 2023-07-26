import os
import json
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
# from wordcloud import WordCloud
# from wordcloud import STOPWORDS
#import matplotlib.pyplot as plotter


'''Class to be used for indexing and searching'''
class MyWhooshSearcher(object):
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()


	'''search() returns the top 120 results from index currently in use'''
	def search(self, queryEntered):
		queryEntered = queryEntered.strip('"')
		with open('traillinkPR.txt', 'r') as f:
			traillinkPR = json.loads(f.read())
			url, title, length, image, state, county, description, activity, surfaces, cloud, difficulty = ([] for _ in range(11))
			with self.indexer.searcher() as search:
				query = MultifieldParser(['length', 'title', 'state', 'county', 'activities', 'content'], schema=self.indexer.schema)
				query = query.parse(queryEntered)
				results = search.search(query, limit=120)
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
						if len_for_diff < 6: difficulty.append('short')
						elif len_for_diff < 12: difficulty.append('medium')
						else: difficulty.append('long')
			styleID = [i for i in range(1,len(url)+1)]
			return url, title, length, image, state, county, description, styleID, activity, surfaces, cloud, difficulty


	'''existing_index() loads an existing index at /myIndex/'''
	def existing_index(self):
		self.indexer = open_dir('myIndex')


	'''build_cloud() uses the given review content to return a word cloud'''
	def build_cloud(self, review, review_cloud_path):
		stopwords = STOPWORDS.update(['trail','trails','mile','miles','ride','road'])
		word_cloud = WordCloud(width=800,
        height=600,
		stopwords=stopwords,
		min_font_size=25,
		max_font_size=180,
		colormap="winter",
		font_path="./static/fonts/Recoleta-Regular.ttf",
		background_color="#ffffff").generate(review)
		plotter.figure(figsize=(8,6), facecolor=None)
		plotter.imshow(word_cloud, interpolation="bilinear")
		plotter.axis('off')
		plotter.tight_layout(pad=0)
		plotter.savefig('./static/images/cloud/' + review_cloud_path)
		plotter.close()


	'''build_index() creates index needed for searching over trail files,
 	calls build_cloud() to generate cloud images aswell'''
	def build_index(self):
		if not os.path.exists('myIndex'):
			os.mkdir('myIndex')
   
		schema = Schema(url=STORED, title=TEXT(stored=True), length=NUMERIC(int, decimal_places=2,stored=True, signed=False), 
			image=STORED, state=KEYWORD(stored=True,commas=True), county=KEYWORD(stored=True,commas=True), 
			description=STORED, trail_surfaces=KEYWORD(commas=True,stored=True), activities=KEYWORD(commas=True,stored=True), content=KEYWORD, cloud_path=STORED)
		
		indexer = create_in('myIndex', schema)
		writer = indexer.writer()
		corpus_path = "./files"
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
					review_cloud_path = name.rstrip('.txt').replace('%','') + '.png'
     
					if os.path.exists('./static/images/cloud/' + review_cloud_path): 
						pass
  
					elif len(review) > 0:
						review = "".join(json_dict['reviews'])
						self.build_cloud(review, review_cloud_path)

					elif 'oregonhikers' in json_dict['url']:
						review = json_dict['description']
						self.build_cloud(review, review_cloud_path)

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
    
