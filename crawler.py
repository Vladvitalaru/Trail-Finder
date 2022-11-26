import requests
from bs4 import BeautifulSoup
import queue
import json
import networkx as nx
from urllib import parse
from urllib import robotparser #json library can dump dictionary into xml, pickle can save as object
import socket
import os
import signal
import re


def main(): 
    print('Enter number of pages to be crawled. (Ex. \'50\')')      #initial input to be passed to our crawler
    num_pages = int(input())
    if num_pages <=0:
        print(f'{num_pages} is not a valid number!')
        os._exit(1)
    print('Enter links to be used as a starting seed separated by spaces. (Ex. \'https://wsu.edu https://www.wikipedia.org https://www.imdb.com\')')
    seed = input()
    seed = seed.split(' ')

    socket.setdefaulttimeout(2)                                     #necessary to avoid hanging indefinitely when parsing poorly formatted robots.txt files
    path = os.path.dirname(__file__)
    os.makedirs(path + '/files', exist_ok=True)

    q = queue.Queue()
    for link in seed:
        q.put((link, ""))
    breadth_first_crawl(q, path, num_pages)

def breadth_first_crawl(q: queue.Queue, path: str, num_pages: int):     #this method follows the basic algorithm outlined in the slides with the exception of not building an index
    url: str
    parent: str
    count: int
    file_path = path + '/files'
    adj_sites = nx.DiGraph()
    visited_sites = set()
    #robot_dict: dict[str, (list[str], robotparser.RobotFileParser)] = {}    #this dictionary will store the hostname as a key and the value will be a tuple containing a list of urls belonging to a hostname as well as a robot object
    traillink_main = parse.urlsplit('https://www.traillink.com')
    robot = get_robot(traillink_main.scheme, traillink_main.hostname)
    count = 0
    signal.signal(signal.SIGINT, ExitHandler((path, adj_sites)))            #allows user to press CTRL+C in order to exit program while running while still saving the adjacency matrix
    hostname_crawlable_dict = {'www.traillink.com': 'https://www.traillink.com/trail/'}
    queue_stop = {'https://www.traillink.com/membership', 'https://www.traillink.com/profiles', 'https://www.traillink.com/mobile-apps' 'https://www.traillink.com/splash/'} #don't bother adding these to the queue

    while (not q.empty() and count < num_pages):
        url, parent = q.get()
        print(f'Popping {url} from Queue')
        split_url = parse.urlsplit(url)
        #print(f'{split_url.hostname}')

        if split_url is not None:
            """if split_url.hostname in robot_dict:
                robot = robot_dict[split_url.hostname][1] #assign pre-created robot object to current url
            else:
                robot = get_robot(split_url.scheme, split_url.hostname)
                robot_dict[split_url.hostname] = (set(), robot)"""

            if robot is not None and url not in visited_sites: #ensures we have a proper robots.txt and url has not been visited yet
                if robot.can_fetch('*', url):
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
                                print(f'Adding {url} to visited list.')
                                file_contents = {}  #empty dict that will store everything we grab from the page
                                visited_sites.add(url)
                                bs = BeautifulSoup(raw_page.text, 'lxml')
                                #check here if crawled page is of correct type
                                if(split_url.hostname in hostname_crawlable_dict and url.startswith(hostname_crawlable_dict[split_url.hostname])):
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
                                    is_crawlable = trail_link_crawl(file_contents, bs, url)
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
                                            if isStopped == False and cleaned_link not in visited_sites:
                                                q.put((cleaned_link, url))
    print(f'Dumping adjacency matrix to \'adjacent_links\' in current directory.')
    nx.write_gpickle(adj_sites, "adjacent_links.gpickle")

def trail_link_crawl(file_contents, bs, url):
    """Will crawl the trail page on traillink, won't work for any other page"""
    stop_list = ['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may', 'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are']
    title = bs.find('title')
    title = title.string.split('|')[0].strip()
    description = bs.find('meta', attrs={'name': 'description'})
    description = description['content']
    review = bs.find_all('p', itemprop='reviewBody')
    fact_dict = {}
    facts = bs.find(class_="trail-facts")
    if facts is None:
        return False
    facts = facts.find_all(class_="small-12 medium-4 columns facts")
    for fact in facts[0].contents:
        if not fact == '\n':
            key = fact.find('strong')
            value = fact.find('span')
            fact_dict[key.string.split(':')[0]] = value.string

    for fact in facts[1]:
        if not fact == '\n':
            key = fact.find('strong')
            value = fact.find('span')
            if key is not None and value is not None:
                fact_dict[key.string.split(':')[0]] = value.string
            else:
                list_activities = []
                activities = key.nextSibling()
                for activity in activities:
                    list_activities.append(activity.text)
                fact_dict['activities'] = list_activities
                break   
            
    list_images = []
    try:
        images = bs.find(id="trail-detail-photos", class_="trail-photos-carousel")
        images = images.find_all(class_="slide medium-4 columns trail-photo")
        for image_url in images:
            image_url = image_url.find('a')
            list_images.append('https:' + image_url.get('href'))
    except AttributeError:
        pass
    content = bs.find(class_="trail-description")
    if content is None:
        return False
    content = content.find(itemprop='description')
    file_contents['url'] = url
    file_contents['title'] = title
    file_contents['description'] = description.rstrip("View maps, amenities, descriptions, reviews, and directions on TrailLink.")
    file_contents['facts'] = fact_dict
    file_contents['images'] = list_images
    file_contents['reviews'] = []       #reviews will be stored in a list
    for r in review: 
        words = r.get_text(" ", strip=True).lower()
        words = words.replace(",","").replace("/", "").replace(":", "").replace("'","").replace(".","").replace('`','').replace('(','').replace(')','')
        for word in stop_list:
            updated = re.sub(rf'\b{word}\b', '', words)
            words = str(updated)
        words = words.split()
        words = ' '.join(words)
        file_contents['reviews'].append(words)
    content = content.get_text(" ", strip=True).lower()
    content = content.replace(",","").replace("/", "").replace(":", "").replace("'","").replace(".","").replace('`','').replace('(','').replace(')','')
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
        nx.write_gpickle(self.my_tuple[1], "adjacent_links.gpickle")
        os._exit(0)


if __name__ == '__main__':
    main()
