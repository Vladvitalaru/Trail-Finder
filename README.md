# Trail Finder Search Engine :evergreen_tree:

### Web application allowing users to search over 20k trails across the US 

![homepage](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/8f3b0f7a-b81e-4b61-bcb6-681bfd6c52e2)

### Live search suggestions based on trail names 

![livesearch](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/5f45ee95-5ac8-45c4-8355-4f7c1f56d89e)


### Trails returned as cards with information such as location, length, images & activities

![results](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/91599409-241a-489f-8df2-1c062ca16a36)


### Word cloud generated based on community reviews from scraped sites

![cloud](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/cfa238f3-fa18-4e87-a764-a338ffb4260a)


## Scraped sites :mag:
Trail cards are built using data scraped from the following trail guides:
- https://www.traillink.com/
- https://www.oregonhikers.org/
- https://opendata.gis.utah.gov/datasets/utah-trails-and-pathways/
- https://ct-deep-gis-open-data-website-ctdeep.hub.arcgis.com/datasets/CTDEEP::hiking-appropriate/
- https://open-data.bouldercolorado.gov/datasets/d7ad8e150c164c32ab1690658f3fa662_4/
- https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-trails-and-sidewalks
- https://public-nps.opendata.arcgis.com/datasets/nps-trails-geographic-coordinate-system-1/


## Development :zap:
- HTML, CSS & Javascript front end
- Built on Flask back end using Jinja2 templating
- Whoosh! for search index
- BeautifulSoup4 for web scraping trail guides

## Dependencies :electric_plug:
Python 3.8 and newer required, 
The following modules were used during development
- Flask==2.2.5
- flask-paginate==2022.1.8
- Jinja2==3.1.2
- lxml==4.9.1
- Whoosh==2.7.4
- matplotlib=3.6.2
- numpy=1.22.3
- wordcloud==1.8.2.2
- beautifulsoup4==4.11.1
- networkx==3.1

## Running locally: :computer:
**By default, an existing search index is used**  
- Using the existing index:
    - In the root folder, set up a local python3.8+ virtual environment and activate it
    - Pip install packages from requirements.txt in your python venv
    - Execute './application.py' within your environment
      
**Build a new index locally:**
 - In application.py
    - Delete/comment ```mySearcher.existing_index()``` in main
    - Delete/comment ```mySearcher.existing_index()``` on line 8
    - Uncomment ```mySearcher.build_index()``` in main
- In mywhoosh.py
  - Uncomment lines 7-9 to import modules for generating new wordclouds
    ```
    from wordcloud import WordCloud
    from wordcloud import STOPWORDS
    import matplotlib.pyplot as plotter
    ```
- After building new index and wordclouds, webpage will run locally
  
## Important :exclamation:
- Requirements.txt only contains the modules used to run on a prebuilt index for deployment, use full dependency list above for generating new index and datasets
- If you wish to change datasets, extract either samplefiles.zip or fullset.zip into the root directory so the .txt files are inside root/files/file.txt
- Indexing trail pages may take some time, there are roughly 25k pages in the fullset.zip and 10k in the samplefiles.zip
- If new trails are added to the dataset, rebuilding the index will generate new wordclouds for those trails
- Pagerank calculator relies on Traillink and Oregontrails being crawled at least once
- All crawlers can be ran separately to generate files for Whoosh

