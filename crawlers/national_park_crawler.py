import json
import csv
import os

csv_attr = {'TRLNAME':1, 'TRALTNAME':2, 'TRLSURFACE':5, 'TRLUSE':8, 'UNITNAME': 14, 'LENGTH':41}
def main():
    """Parses specified csv file then outputs json strings for Whoosh"""
    existing_trails = {}
    with open("./csv/NPS_-_Trails_-_Geographic_Coordinate_System.csv", 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        next(csv_reader) #skip header
        for tuple in csv_reader:
            if tuple[csv_attr['TRLNAME']] != '':
                parse_line(tuple, existing_trails)
    path = os.path.dirname(__file__)
    path = path + '/files'
    os.makedirs(path, exist_ok=True)
    for name, trail in existing_trails.items():
        write_files(name, trail, path)
def parse_line(tuple, existing_trails):
    name = tuple[csv_attr['TRLNAME']]
    if tuple[csv_attr['TRALTNAME']] != '':
        if tuple[csv_attr['TRALTNAME']] != 'None':
            name = name + '_' + tuple[csv_attr['TRALTNAME']]
    if name not in existing_trails:
        existing_trails[name] = tuple
    else:
        trail = existing_trails[name]
        trail[csv_attr['LENGTH']] = float(trail[csv_attr['LENGTH']]) + float(tuple[csv_attr['LENGTH']])
        existing_trails[name] = trail
def write_files(name, trail, path):
    fact_dict = {}
    fact_dict['States'] = ''
    fact_dict['Counties'] = ''
    fact_dict['Length'] = str(round(float(trail[csv_attr['LENGTH']]), 2))
    fact_dict['Trail surfaces'] = trail[csv_attr['TRLSURFACE']]
    activity_list = []
    activities = trail[csv_attr['TRLUSE']].split('|')
    for activity in activities:
        if 'Hik' in activity:
            activity_list.append('Hiking')
        elif 'All' in activity:
            activity_list.append('ATV')
        elif 'Motorcycle' in activity:
            activity_list.append('Motorcycling')
        elif 'Snowmob' in activity:
            activity_list.append('Snowmobiling')
        elif 'Snowsho' in activity:
            activity_list.append('Snowshoeing')
        elif 'Cross' in activity:
            activity_list.append('Cross-country Skiing')
        elif 'Dog Sled' in activity:
            activity_list.append('Dogsledding')
    fact_dict['activities'] = activity_list
    file_contents = {}
    file_contents['url'] = 'https://public-nps.opendata.arcgis.com/datasets/nps-trails-geographic-coordinate-system-1/'
    file_contents['title'] = name.replace('_', ' - ')
    file_contents['description'] = trail[csv_attr['UNITNAME']] + '\nGovernment Index Trail'
    file_contents['facts'] = fact_dict
    file_contents['images'] = []
    file_contents['reviews'] = [] 
    file_contents['content'] = name.replace('_',' ')
    file_name = name.replace("/", "").replace(":", "").replace("?", "").replace(" ", "_")

    with open(f'{path}/{file_name}.txt', 'w') as f:
        json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
if __name__ == '__main__':
    main()
 
