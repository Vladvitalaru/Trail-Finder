import requests
from bs4 import BeautifulSoup
from collections import deque
import json
import networkx as nx
from urllib import parse
from urllib import robotparser #json library can dump dictionary into xml, pickle can save as object
import socket
import os
import signal
import re


def main(): 
    """Crawls oregonhikers.org and outputs trail pages into a file"""
    num_pages = 5000
    seed = ['https://www.oregonhikers.org/'] #input()
    #seed = ['https://www.oregonhikers.org/field_guide/Wahclella_Falls_Hike']

    socket.setdefaulttimeout(2)                                     #necessary to avoid hanging indefinitely when parsing poorly formatted robots.txt files
    path = os.path.dirname(__file__)
    os.makedirs(path + '/files', exist_ok=True)

    q = deque()
    for link in seed:
        q.append((link, ""))
    breadth_first_crawl(q, path, num_pages)

def breadth_first_crawl(q: deque, path: str, num_pages: int):     #this method follows the basic algorithm outlined in the slides with the exception of not building an index
    url: str
    parent: str
    count: int
    file_path = path + '/files'
    #adj_sites = nx.read_gpickle("adjacent_links.gpickle")
    adj_sites = nx.DiGraph()
    visited_sites = set()
    #robot_dict: dict[str, (list[str], robotparser.RobotFileParser)] = {}    #this dictionary will store the hostname as a key and the value will be a tuple containing a list of urls belonging to a hostname as well as a robot object
    link_main = parse.urlsplit('https://www.oregonhikers.org/')
    #robot = get_robot(link_main.scheme, link_main.hostname)
    count = 0
    signal.signal(signal.SIGINT, ExitHandler((path, adj_sites)))            #allows user to press CTRL+C in order to exit program while running while still saving the adjacency matrix
    hostname_crawlable_dict = {'www.oregonhikers.org': 'https://www.oregonhikers.org/field_guide/'}

    queue_stop = {'forum', 'User:', 'Talk:', 'File:', 'Help:'} 

    while (q and count < num_pages):
        url, parent = q.popleft()
        print(f'Popping {url} from Queue')
        
        split_url = parse.urlsplit(url)

        if split_url is not None and url not in visited_sites:
            visited_sites.add(url)
            print(f'Currently in: {url}')
            #delay_time = robot.crawl_delay('*')
            #if delay_time is not None and delay_time <= 15:             #limiting to 15 because certain websites have 30 seconds of delay yet don't ban for breaking the rule
                #time.sleep(delay_time)
            raw_page = get_page(url)
            if raw_page is not None:
                content_type = raw_page.headers.get('content-type')
                if content_type is not None:
                    print(f'URL is of type: {content_type}')
                    if 'text/html' in content_type:                     #continue loop if page grabbed is not of correct type
                        file_contents = {}  #empty dict that will store everything we grab from the page
                        
                        bs = BeautifulSoup(raw_page.text, 'lxml')
                        isCrawlable = url.endswith('_Hike')
                        if(split_url.hostname in hostname_crawlable_dict and isCrawlable == True):
                            if parent != "":
                                if not adj_sites.has_node(parent):       #check if nodes already exist
                                    adj_sites.add_node(parent) 
                                if not adj_sites.has_node(url):
                                    adj_sites.add_node(url)
                                adj_sites.add_edge(parent, url)         #add edge between nodes for pagerank
                            count += 1
                            print(f'Number of pages crawled: {count}')
                            url_filename = url.replace("/", "").replace(":", "").replace("?", "")
                            if len(url_filename) >= 200:                        #hash filename to comfortably fit max filename size
                                url_filename = str(hash(url_filename))
                            try:
                                is_crawlable = oregon_hikers_crawl(file_contents, bs, url)
                            except:
                                is_crawlable = False
                            if is_crawlable is True:
                                with open(f'{file_path}/{url_filename}.txt', 'w') as f:
                                    json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
                            else:
                                count -=1               #wasn't able to crawl page, have to decrement count
                        for link in bs.find_all('a'): #gets all anchor text
                            cleaned_link:str = link.get('href') #ensure it's a trail finder link here
                            if cleaned_link is not None and cleaned_link != "":
                                if cleaned_link[0] == '/':
                                    cleaned_link = parse.urljoin(url, cleaned_link)
                                cleaned_link = parse.urlsplit(cleaned_link)
                                cleaned_link_domain = cleaned_link.hostname
                                if cleaned_link.fragment != '' or cleaned_link.query != '':
                                    cleaned_link = parse.SplitResult(cleaned_link.scheme, cleaned_link.netloc, cleaned_link.path, '', '')
                                cleaned_link = parse.urlunsplit(cleaned_link)
                                if 'http' in cleaned_link and cleaned_link_domain == split_url.hostname: #check if within domain
                                    isStopped = False
                                    for stop_link in queue_stop:
                                        if stop_link in cleaned_link:
                                            isStopped = True
                                            break
                                    if isStopped == False and cleaned_link not in visited_sites and 'Talk:' not in cleaned_link:
                                        q.append((cleaned_link, url))
        elif url not in visited_sites: #url can't be split
            visited_sites.add(url)

    print(f'Dumping adjacency matrix to \'adjacent_links\' in current directory.')
    nx.write_gpickle(adj_sites, "adjacent_links_oregonhikers.gpickle")

def oregon_hikers_crawl(file_contents, bs, url):
    """Will crawl the trail page on oregon hikers, won't work for any other page"""
    stop_list = ['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may', 'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are']
    title = bs.find(title='Main Page').string
    description_obj = bs.find_all("p")
    description = [] 
    for line in description_obj:
        if line.text != '\n':
            description.append(line.text.strip())
            break #only getting one line
    description = "".join(description).replace('\n','')
    review = []
    fact_dict = {}
    facts = bs.find(class_="mw-content-ltr")
    if facts is None:
        return False
    facts = facts.find("ul")
    for fact in facts.contents:
        if not fact == '\n':
            try:
                line = fact.text.replace('\n','').split(':')
                key = line[0].strip().lower()
                value = line[1].strip()
                fact_dict[key] = value
            except:
                continue
            
    list_images = []
    try:
        images = bs.find(id="mw-content-text")
        #images = images.find_all(class_="slide medium-4 columns trail-photo")
        images = images.find_next(class_="thumb tright")
        images = images.find("img")
        image_url = parse.urljoin('https://www.oregonhikers.org/', images.get('src'))
        list_images.append(image_url)
    except AttributeError:
        pass
    activities = []
    try:
        if 'Yes' in fact_dict['backpackable']:
            activities.append('Backpackable')
    except:
        pass
    try:
        if 'Yes' in fact_dict['family friendly']:
            activities.append('Family Friendly')
    except:
        pass
    new_fact_dict = {}
    new_fact_dict['States'] = 'Oregon'
    new_fact_dict['Counties'] = ''
    new_fact_dict['Length'] = fact_dict['distance'].split()[0]
    new_fact_dict['Trail surfaces'] = ''
    
    
    file_contents['url'] = url
    file_contents['title'] = title
    file_contents['description'] = description
    file_contents['facts'] = new_fact_dict
    file_contents['images'] = list_images
    file_contents['reviews'] = []       #no reviews
    content = bs.get_text(" ", strip=True).lower()
    content = content.replace(",","").replace("/", "").replace(":", "").replace("'","").replace(".","").replace('`','').replace('(','').replace(')','').replace('|','')
    for word in stop_list:
        updated = re.sub(rf'\b{word}\b', '', content)
        content = str(updated)
    content = content.split()
    content = ' '.join(content)
    file_contents['content'] = content
    return True
                                
            
def get_robot(scheme: str, hostname: str): #tries to create a robot object, if an exception occurs returns none
        robot = robotparser.RobotFileParser()
        try:
            robot.set_url(parse.urljoin(scheme + '://' + hostname, 'robots.txt'))
            robot.read()
            return robot
        except:
            print(f'Failed to grab robots.txt for {hostname}.')
            return None
def get_page(url: str):
        try:
            return requests.get(url,timeout=3)
        except:
            print(f'Failed to get page for {url}.')
            return None

class ExitHandler:                          #saves current state of adjacency matrix to json then exits program
    def __init__(self, tuple):
        self.my_tuple = tuple
    def __call__(self, signo, frame):
        print(f'Dumping adjacency matrix to \'adjacent_links\' in current directory.')
        nx.write_gpickle(self.my_tuple[1], "adjacent_links_oregonhikers.gpickle")
        os._exit(0)


if __name__ == '__main__':
    main()
