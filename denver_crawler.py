import json
import csv
import os

csv_attr = {'LOCATION':0, 'TRAIL_NAME':2, 'SURFACE_TYPE':6, 'LENGTH_MILE':7, 'CLASS_CATEGORY': 15}
def main():
    existing_trails = {}
    with open("./csv/trails_and_sidewalks.csv", 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        next(csv_reader) #skip header
        for tuple in csv_reader:
            if tuple[csv_attr['LENGTH_MILE']] != 'None':
                parse_line(tuple, existing_trails)
    path = os.path.dirname(__file__)
    path = path + '/files'
    os.makedirs(path, exist_ok=True)
    for name, trail in existing_trails.items():
        write_files(name, trail, path)
def parse_line(tuple, existing_trails):
    name = tuple[csv_attr['LOCATION']]
    if tuple[csv_attr['TRAIL_NAME']] != 'None':
        name = name + '_' + tuple[csv_attr['TRAIL_NAME']]
    if name not in existing_trails:
        existing_trails[name] = tuple
    else:
        trail = existing_trails[name]
        trail[csv_attr['LENGTH_MILE']] = float(trail[csv_attr['LENGTH_MILE']]) + float(tuple[csv_attr['LENGTH_MILE']])
        existing_trails[name] = trail
def write_files(name, trail, path):
    fact_dict = {}
    fact_dict['States'] = 'Colorado'
    fact_dict['Counties'] = 'Denver'
    fact_dict['Length'] = str(round(float(trail[csv_attr['LENGTH_MILE']]), 1))
    fact_dict['Trail surfaces'] = trail[csv_attr['SURFACE_TYPE']]
    activity_list = []
    if 'TRL' in trail[csv_attr['CLASS_CATEGORY']]:
        activity_list.append('Hiking')
    else:
        activity_list.append('Walking')
    
        
    fact_dict['activities'] = activity_list
    file_contents = {}
    file_contents['url'] = 'https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-trails-and-sidewalks'
    file_contents['title'] = name.replace('_', ' - ')
    file_contents['description'] = 'Government Index Trail'
    file_contents['facts'] = fact_dict
    file_contents['images'] = []
    file_contents['reviews'] = [] 

    file_contents['content'] = name
    file_name = name.replace("/", "").replace(":", "").replace("?", "").replace(" ", "_")
    with open(f'{path}/denver_{file_name}.txt', 'w') as f:
        json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
if __name__ == '__main__':
    main()
 
