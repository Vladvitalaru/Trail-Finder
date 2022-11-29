import json
import csv
import os

csv_attr = {'DOGS':16, 'TRAIL_NAME':13, 'BICYCLES':2, 'LENGTH_MILE':11, 'TRAIL_TYPE': 4, 'HORSES': 8, 'DOGREG': 18}
def main():
    existing_trails = {}
    with open("./csv/OSMP_Trails.csv", 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        next(csv_reader) #skip header
        for tuple in csv_reader:
            if tuple[csv_attr['LENGTH_MILE']] != 'None':
                parse_line(tuple, existing_trails)
    path = os.path.dirname(__file__)
    path = path + '/files'
    os.makedirs(path, exist_ok=True)
    for trail in existing_trails:
        write_files(existing_trails[trail], path)
def parse_line(tuple, existing_trails):
    if tuple[csv_attr['TRAIL_NAME']] not in existing_trails:
        existing_trails[tuple[csv_attr['TRAIL_NAME']]] = tuple
    else:
        trail = existing_trails[tuple[csv_attr['TRAIL_NAME']]]
        trail[csv_attr['LENGTH_MILE']] = float(trail[csv_attr['LENGTH_MILE']]) + float(tuple[csv_attr['LENGTH_MILE']])
        existing_trails[tuple[csv_attr['TRAIL_NAME']]] = trail
    
def write_files(trail, path):
    fact_dict = {}
    fact_dict['States'] = 'Colorado'
    fact_dict['Counties'] = 'Boulder'
    fact_dict['Length'] = str(round(float(trail[csv_attr['LENGTH_MILE']]), 2))
    fact_dict['Trail surfaces'] = ''
    activity_list = []
    #stopped here
    if 'Hiking' in trail[csv_attr['TRAIL_TYPE']]:
        activity_list.append('Hiking')
    elif 'Multi' in trail[csv_attr['TRAIL_TYPE']]:
        activity_list.append('Multi-Use')
    else:
        activity_list.append('Gliding Access')
    if trail[csv_attr['BICYCLES']] == 'Yes':
        activity_list.append('Biking')
    if trail[csv_attr['HORSES']] == 'Yes':
        activity_list.append('Horseback Riding')
    if trail[csv_attr['DOGS']] == 'Yes':
        activity_list.append('Dog Walking (' + trail[csv_attr['DOGREG']] + ')')
    
        
    fact_dict['activities'] = activity_list
    file_contents = {}
    file_contents['url'] = 'https://open-data.bouldercolorado.gov/datasets/d7ad8e150c164c32ab1690658f3fa662_4/'
    file_contents['title'] = trail[csv_attr['TRAIL_NAME']]
    file_contents['description'] = 'Government Index Trail'
    file_contents['facts'] = fact_dict
    file_contents['images'] = []
    file_contents['reviews'] = [] 

    file_contents['content'] = trail[csv_attr['TRAIL_NAME']]
    file_name = trail[csv_attr['TRAIL_NAME']].replace("/", "").replace(":", "").replace("?", "").replace(" ", "_")
    with open(f'{path}/boulder_{file_name}.txt', 'w') as f:
        json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
if __name__ == '__main__':
    main()
 
