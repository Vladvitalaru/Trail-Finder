import json
import csv
import os
from enum import Enum
csv_attr = {'PrimaryName':1, 'DesignatedUses':4, 'SurfaceType':5, 'Class':6, 'CartoCode': 7, 'HorseAllowed': 9, 'MotorizedAllowed': 10, 'County': 15, 'SHAPE_Length':26}
def main():
    existing_trails = {}
    with open("./Utah_Trails_and_Pathways.csv", 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        next(csv_reader) #skip header
        for tuple in csv_reader:
            if tuple[csv_attr['PrimaryName']] != '':
                parse_line(tuple, existing_trails)
    path = os.path.dirname(__file__)
    path = path + '/files'
    os.makedirs(path, exist_ok=True)
    for trail in existing_trails:
        write_files(existing_trails[trail], path)
def parse_line(tuple, existing_trails):
    if tuple[csv_attr['PrimaryName']] not in existing_trails:
        existing_trails[tuple[csv_attr['PrimaryName']]] = tuple
    else:
        trail = existing_trails[tuple[csv_attr['PrimaryName']]]
        trail[csv_attr['SHAPE_Length']] = float(trail[csv_attr['SHAPE_Length']]) + float(tuple[csv_attr['SHAPE_Length']])
        existing_trails[tuple[csv_attr['PrimaryName']]] = trail
def write_files(trail, path):
    fact_dict = {}
    fact_dict['States'] = 'Utah'
    fact_dict['Counties'] = trail[csv_attr['County']].lower().capitalize()
    fact_dict['Length'] = str(float(trail[csv_attr['SHAPE_Length']]) / 5280)
    fact_dict['Trail surfaces'] = trail[csv_attr['SurfaceType']]
    if trail[csv_attr['CartoCode']].startswith('1'):
        fact_dict['activities'] = ['Hiking']
    elif trail[csv_attr['CartoCode']].startswith('2'):
        fact_dict['activities'] = ['Hiking', 'Biking', 'Single Track']
    elif trail[csv_attr['CartoCode']].startswith('3'):
        fact_dict['activities'] = ['Hiking', 'Biking']
    elif trail[csv_attr['CartoCode']].startswith('4'):
        fact_dict['activities'] = ['Hiking', 'Biking', 'Road-concurrent']
    else:
        fact_dict['activities'] = []
    file_contents = {}
    file_contents['url'] = 'https://opendata.gis.utah.gov/datasets/utah-trails-and-pathways/'
    file_contents['title'] = trail[csv_attr['PrimaryName']]
    file_contents['description'] = 'Government Index Trail'
    file_contents['facts'] = fact_dict
    file_contents['images'] = []
    file_contents['reviews'] = [] 
    file_contents['content'] = "".join(trail[0:16])
    file_name = trail[csv_attr["PrimaryName"]].replace("/", "").replace(":", "").replace("?", "").replace(" ", "_")
    with open(f'{path}/{file_name}.txt', 'w') as f:
        json.dump(file_contents, f) #can't use pickle here without changing how file contents are stored
if __name__ == '__main__':
    main()
 
