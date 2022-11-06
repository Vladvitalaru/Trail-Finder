import requests
from bs4 import BeautifulSoup
import queue
import json
from urllib import parse
from urllib import robotparser #json library can dump dictionary into xml, pickle can save as object
import time
import socket
import os
import signal


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
        q.put(link)
    breadth_first_crawl(q, path, num_pages)

def breadth_first_crawl(q: queue.Queue, path: str, num_pages: int):     #this method follows the basic algorithm outlined in the slides with the exception of not building an index
    url: str
    count: int
    file_path = path + '/files'
    adj_sites = {}
    robot_dict: dict[str, (list[str], robotparser.RobotFileParser)] = {}    #this dictionary will store the hostname as a key and the value will be a tuple containing a list of urls belonging to a hostname as well as a robot object
    count = 0
    signal.signal(signal.SIGINT, ExitHandler((path, adj_sites)))            #allows user to press CTRL+C in order to exit program while running while still saving the adjacency matrix
    hostname_crawlable_dict = {'www.traillink.com': 'https://www.traillink.com/trail/'}

    while (not q.empty() and count < num_pages):
        url = q.get()
        print(f'Popping {url} from Queue')
        split_url = parse.urlsplit(url)
        #print(f'{split_url.hostname}')

        if split_url is not None:
            if split_url.hostname in robot_dict:
                robot = robot_dict[split_url.hostname][1] #assign pre-created robot object to current url
            else:
                robot = get_robot(split_url.scheme, split_url.hostname)
                robot_dict[split_url.hostname] = ([], robot)

            if robot is not None and url not in robot_dict[split_url.hostname][0]: #ensures we have a proper robots.txt and url has not been visited yet
                if robot.can_fetch('*', url):
                    print(f'Currently in: {url}')
                    delay_time = robot.crawl_delay('*')
                    if delay_time is not None and delay_time <= 15:             #limiting to 15 because certain websites have 30 seconds of delay yet don't ban for breaking the rule
                        time.sleep(delay_time)
                    raw_page = get_page(url)
                    if raw_page is not None:
                        content_type = raw_page.headers.get('content-type')
                        if content_type is not None:
                            print(f'URL is of type: {content_type}')
                            if 'text/html' in content_type:                     #continue loop if page grabbed is not of correct type
                                print(f'Adding {url} to visited list.')
                                file_contents = {}  #empty dict that will store everything we grab from the page
                                robot_dict[split_url.hostname][0].append(url)
                                bs = BeautifulSoup(raw_page.text, 'lxml')
                                #check here if crawled page is of correct type
                                if(split_url.hostname in hostname_crawlable_dict and url.startswith(hostname_crawlable_dict[split_url.hostname])):
                                    count += 1
                                    print(f'Number of pages crawled: {count}')
                                    url_filename = url.replace("/", "").replace(":", "")
                                    if len(url_filename) >= 200:                        #hash filename to fit linux max filename size
                                        url_filename = str(hash(url_filename))
                                    trail_link_crawl(file_contents, bs, url)
                                    with open(f'{file_path}/{url_filename}.txt', 'w') as f:
                                        json.dump(file_contents, f) #instead of writing line by line, why not take advantage of JSON?
                                for link in bs.find_all('a'): #gets all anchor text
                                    cleaned_link = link.get('href')
                                    if cleaned_link is not None and cleaned_link != "":
                                        if cleaned_link[0] == '/':
                                            cleaned_link = parse.urljoin(url, cleaned_link)
                                            cleaned_link_domain = parse.urlsplit(cleaned_link).hostname
                                        if 'http' in cleaned_link and cleaned_link_domain == split_url.hostname:
                                            if cleaned_link not in adj_sites:       #create new linked list to store adjacencies
                                                adj_sites[cleaned_link] = [url]
                                            else:                                   #append to existing list and replace
                                                if url not in adj_sites[cleaned_link]:
                                                    adj_sites[cleaned_link].append(url) 
                                            q.put(cleaned_link)
    print(f'Dumping adjacency matrix to \'adjacent_links\' in current directory.')
    with open(f'{path}/adjacent_links', 'w') as f:
        json.dump(adj_sites, f)

def trail_link_crawl(file_contents, bs, url):
    """Will crawl the trail page on traillink, won't work for any other page"""
    title = bs.find('title')
    description = bs.find('meta', attrs={'name': 'description'})
    description = description['content']
    review = bs.find_all('p', itemprop='reviewBody')
    facts = bs.find(class_="trail-facts")
    facts = facts.find_all(class_="small-12 medium-4 columns facts")
    fact_dict = {}
    for fact in facts[0].contents:
        if not fact == '\n':
            key = fact.find('strong')
            value = fact.find('span')
            fact_dict[key.string] = value.string

    for fact in facts[1]:
        if not fact == '\n':
            key = fact.find('strong')
            value = fact.find('span')
            if key is not None and value is not None:
                fact_dict[key.string] = value.string
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
    content = content.find(itemprop='description')
    file_contents['url'] = url
    file_contents['title'] = title.string
    file_contents['description'] = description
    file_contents['facts'] = fact_dict
    file_contents['images'] = list_images
    file_contents['reviews'] = []       #reviews will be stored in a list
    for r in review:
        file_contents['reviews'].append("".join(r.stripped_strings))
    file_contents['content'] = content.get_text(" ", strip=True)
    return
                                
            
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
        with open(f'{self.my_tuple[0]}/adjacent_links', 'w') as f:
            json.dump(self.my_tuple[1], f)
        os._exit(0)


if __name__ == '__main__':
    main()
