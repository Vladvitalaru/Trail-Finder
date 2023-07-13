# Trail Finder Search Engine :evergreen_tree:

### Web application which allows users to search for trails across the US

![homepage](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/22fbd1a9-849d-4773-83ee-779d8022c079)

### Live search suggestions based on trail names 

![livesearch](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/dfa24894-18c2-49d3-8abc-d01ca0a5a834)


### Trails returned as cards with information such as location, length, images & activities

![results](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/1bc7f104-8950-40b2-a7ba-c6433f55bbc4)


### Word cloud generated based on reviews from scraped sites

![cloud](https://github.com/Vladvitalaru/Trail-Finder/assets/78878935/1d3c399c-01f9-4af3-92d8-cabcf0ed8fbc)


## Scraped sites :mag:
Trail cards are built using data scraped from the following sites:
- https://www.traillink.com/
- https://www.oregonhikers.org/
- https://opendata.gis.utah.gov/datasets/utah-trails-and-pathways/
- https://ct-deep-gis-open-data-website-ctdeep.hub.arcgis.com/datasets/CTDEEP::hiking-appropriate/
- https://open-data.bouldercolorado.gov/datasets/d7ad8e150c164c32ab1690658f3fa662_4/
- https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-trails-and-sidewalks
- https://public-nps.opendata.arcgis.com/datasets/nps-trails-geographic-coordinate-system-1/


## Stack :zap:
- Built on Flask back end
- Jinja templating
- Whoosh! for search engine
- Vanilla HTML, CSS & Javascript front end

## Dependencies :electric_plug:
Python 3.8 and newer required, 
The following modules were used
- Flask
- flask-paginate
- Jinja2
- lxml
- Whoosh
- matplotlib
- numpy
- pandas
- wordcloud
- beautifulsoup4

## Important :exclamation:
- Extract either samplefiles.zip or fullset.zip in the root directory so the .txt files are inside root/files/file.txt
- Indexing trail pages may take some time, there are roughly 25k pages in the fullset.zip and 10k in the samplefiles.zip
- Will also generate word cloud reviews if no matching filename for the cloud image is found.
- All crawlers can be ran separately to generate files for Whoosh
- Pagerank calculator relies on Traillink and Oregontrails being crawled at least once

## To Run locally:
- **By default, an existing index is used**
- If using the existing index:
    - Run 'python ./server_whoosh.py'
- If building a new index:
    - Go into server_whoosh.py, comment out 'mySearcher.existing_index()'
    - Uncomment 'mySearcher.build_index()'
    - Run 'python ./server_whoosh.py'
