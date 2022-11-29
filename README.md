# Trail Finder Search Engine :evergreen_tree:

### Web application which allows users to search for trails across the US

![frontpage](https://user-images.githubusercontent.com/78878935/204413857-045650f7-d682-4f68-915f-3f5c63ed30f1.JPG)

### Live search suggestions based on trail names 

![livesearch](https://user-images.githubusercontent.com/78878935/204431279-6573761e-7177-4b3c-b584-d1966a45df16.JPG)

### Trails returned as cards with information such as location, length, images & activities

![results](https://user-images.githubusercontent.com/78878935/204414248-0098bd03-6b1f-49a5-9710-619fe5c9939c.JPG)

### Word cloud generated based on reviews from scraped sites

![cloud](https://user-images.githubusercontent.com/78878935/204432064-77ee3337-628e-4fce-9f4c-508066416f99.JPG)

### Advanced search filters may be used to narrow search 

![advsearch](https://user-images.githubusercontent.com/78878935/204431056-18beb70b-757f-40bd-b4d2-1dbd3fc500e8.JPG)

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
Pip install the following modules:
- Flask
- flask-paginate
- Whoosh
- matplotlib
- pandas
- wordcloud

## Important :exclamation:
- Extract either samplefiles.zip or fullset.zip in the root directory so the .txt files are inside root/files/file.txt
- Indexing trail pages may take some time, there are roughly 25k pages in the fullset.zip and 10k in the samplefiles.zip
- Will also generate word cloud reviews if no matching filename for the cloud image is found.
- All crawlers can be ran separately to generate files for Whoosh
- Pagerank calculator relies on Traillink and Oregontrails being crawled at least once

## To Run:
- If using the existing index:
    - Run 'python ./server_whoosh.py'
- If building a new index:
    - Go into server_whoosh.py, comment out 'mySearcher.existing_index()'
    - uncomment 'mySearcher.build_index()'
    - Run 'python ./server_whoosh.py'
