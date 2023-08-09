"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    content_csv = []
    for item in results:
        tmp = {
            "datetime_utc": item.time,
            "distance_au": item.distance,
            "velocity_km_s": item.velocity,
            "designation": item.neo.designation,
            "name": item.neo.name,
            "diameter_km": item.neo.diameter,
            "potentially_hazardous": item.neo.hazardous
        }
        content_csv.append(tmp)

    with open(filename, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content_csv)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    content_json = []
    for item in results:
        tmp = {
            "datetime_utc": datetime_to_str(item.time),
            "distance_au": item.distance,
            "velocity_km_s": item.velocity,
            "neo": {
                "designation": str(item.neo.designation),
                "name": item.neo.name,
                "diameter_km": item.neo.diameter,
                "potentially_hazardous": item.neo.hazardous
            }
        }
        content_json.append(tmp)

    with open(filename, 'w') as outfile:
        json.dump(content_json, outfile, indent=2)
