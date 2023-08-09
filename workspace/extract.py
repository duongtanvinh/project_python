"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    output_csv_neo_obj = []
    with open(neo_csv_path, 'r') as line_in_file:
        reader = csv.reader(line_in_file)
        next(line_in_file)
        for row in reader:
            neo = NearEarthObject(row[3], row[4], row[15], row[7])
            output_csv_neo_obj.append(neo)

    return output_csv_neo_obj


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.
    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    ouput_json_cla_obj = []
    with open(cad_json_path, 'r') as line_in_file:
        content = json.load(line_in_file)

    for row_data in content["data"]:
        cla = CloseApproach(row_data[0], row_data[3], row_data[4], row_data[7])
        ouput_json_cla_obj.append(cla)

    return ouput_json_cla_obj
