# Trail Finder Search Engine :evergreen_tree:

**Trail Finder is a web application which allows users to search for trails across the US**

![frontpage](https://user-images.githubusercontent.com/78878935/204413857-045650f7-d682-4f68-915f-3f5c63ed30f1.JPG)

**Trails are returned as cards with information such as location, length, images, activities & review word clouds**

![results](https://user-images.githubusercontent.com/78878935/204414248-0098bd03-6b1f-49a5-9710-619fe5c9939c.JPG)

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
- Indexing and creation of word cloud images may take some time, there are roughly 25k pages in the fullset.zip and 7k in the samplefiles.zip
