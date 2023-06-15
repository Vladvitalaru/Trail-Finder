import json
import csv
import os

csv_attr = {'TRAILSYSID':1, 'TRAILNAME':2, 'TRAILCLASS':4, 'TRAILSURF':5, 'PUBACCESS': 7, 'HIKE': 8, 'WALK':9, 'RUN': 10, 'INLINSKATE':11, 'BIKE': 12, 'MTNBIKE': 13, 'MOTORBIKE': 14, 'ALLTERVEH':15, 'SNOWMOBILE': 16, 'CROSSCSKI':17, 'EQUESTRIAN':18, 'ADAACCESS':19, 'DOGLEASH':20, 'DOGUNLEASH':21, 'Shape__Length':28}
def main():
    """Parses specified csv file then outputs json strings for Whoosh"""
    existing_trails = {}
    with open("./csv/DEEP_Trails_Set.csv", 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        next(csv_reader) #skip header
        for tuple in csv_reader:
            if tuple[csv_attr['TRAILNAME']] != '' and tuple[csv_attr['Shape__Length']] != '':
                parse_line(tuple, existing_trails)
    path = os.path.dirname(__file__)
    path = path + '/files'
    os.makedirs(path, exist_ok=True)
    for trail in existing_trails:
        write_files(existing_trails[trail], path)
def parse_line(tuple, existing_trails):
    if tuple[csv_attr['TRAILNAME']] not in existing_trails:
        existing_trails[tuple[csv_attr['TRAILNAME']]] = tuple
    else:
        trail = existing_trails[tuple[csv_attr['TRAILNAME']]]
        trail[csv_attr['Shape__Length']] = float(trail[csv_attr['Shape__Length']]) + float(tuple[csv_attr['Shape__Length']])
        existing_trails[tuple[csv_attr['TRAILNAME']]] = trail
def write_files(trail, path):
    fact_dict = {}
    fact_dict['States'] = 'Connecticut'
    fact_dict['Counties'] = ''
    fact_dict['Length'] = str(round(float(trail[csv_attr['Shape__Length']]) / 5280, 1))
    fact_dict['Trail surfaces'] = trail[csv_attr['TRAILSURF']]
    activity_list = []
    #stopped here
    if trail[csv_attr['PUBACCESS']] == 'True':
        activity_list.append('Public Access')
    if trail[csv_attr['HIKE']] == 'True':
        activity_list.append('Hiking')
    if trail[csv_attr['WALK']] == 'True':
        activity_list.append('Walking')
    if trail[csv_attr['RUN']] == 'True':
        activity_list.append('Running')
    if trail[csv_attr['INLINSKATE']] == 'True':
        activity_list.append('Inlike Skating')
    if trail[csv_attr['BIKE']] == 'True':
        activity_list.append('Biking')
    if trail[csv_attr['MTNBIKE']] == 'True':
        activity_list.append('Mountain Biking')
    if trail[csv_attr['MOTORBIKE']] == 'True':
        activity_list.append('Motor Biking')
    if trail[csv_attr['ALLTERVEH']] == 'True':
        activity_list.append('ATV')
    if trail[csv_attr['SNOWMOBILE']] == 'True':
        activity_list.append('Snowmobiling')
    if trail[csv_attr['RUN']] == 'True':
        activity_list.append('Cross Country Skiing')
    if trail[csv_attr['EQUESTRIAN']] == 'True':
        activity_list.append('Horseback Riding')
    if trail[csv_attr['ADAACCESS']] == 'True':
        activity_list.append('ADA Accessible')
    if trail[csv_attr['DOGUNLEASH']] == 'True':
        activity_list.append('Dog Walking (Unleashed)')
    elif trail[csv_attr['DOGLEASH']] == 'True':
        activity_list.append('Dog Walking (Leashed)')
        
    fact_dict['activities'] = activity_list
    file_contents = {}
    file_contents['url'] = 'https://ct-deep-gis-open-data-website-ctdeep.hub.arcgis.com/datasets/CTDEEP::hiking-appropriate/'
    file_contents['title'] = trail[csv_attr['TRAILNAME']]
    file_contents['description'] = 'Government Index Trail'
    file_contents['facts'] = fact_dict
    file_contents['images'] = []
    file_contents['reviews'] = [] 
    content = [trail[csv_attr['TRAILNAME']]]
    content.append(trail[csv_attr['TRAILCLASS']])
    content.append(" ".join(activity_list))

    file_contents['content'] = " ".join(content)
    file_name = trail[csv_attr["TRAILNAME"]].replace("/", "").replace(":", "").replace("?", "").replace(" ", "_")
    with open(f'{path}/connecticut_{file_name}.txt', 'w') as f:
        json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
if __name__ == '__main__':
    main()
 
