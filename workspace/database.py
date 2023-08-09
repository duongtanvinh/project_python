"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
import math

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        for neo in self._neos:
            for approache in self._approaches:
                if neo.designation == approache._designation:
                    neo.approaches.append(approache)
                    approache.neo = neo

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if designation == neo.designation:
                return neo
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if name == neo.name:
                return neo
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            match_filter = True

            if "date" in filters:
                if approach.time.date() != filters["date"]:
                    match_filter = False

            if "start_date" in filters and "end_date" not in filters:
                if approach.time.date() < filters["start_date"]:
                    match_filter = False

            if "start_date" not in filters and "end_date" in filters:
                if approach.time.date() > filters["end_date"]:
                    match_filter = False

            if "start_date" in filters and "end_date" in filters:
                if  approach.time.date() < filters["start_date"] or approach.time.date() > filters["end_date"]:
                    match_filter = False
            
            if "distance_min" in filters and "distance_max" not in filters:
                if approach.distance < float(filters["distance_min"]):
                    match_filter = False

            if "distance_min" not in filters and "distance_max" in filters:
                if approach.distance > float(filters["distance_max"]):
                    match_filter = False

            if "distance_min" in filters and "distance_max" in filters:
                if approach.distance < float(filters["distance_min"]) or approach.distance > float(filters["distance_max"]):
                    match_filter = False
            
            if "velocity_min" in filters and "velocity_max" not in filters:
                if approach.velocity < float(filters["velocity_min"]):
                    match_filter = False

            if "velocity_min" not in filters and "velocity_max" in filters:
                if approach.velocity > float(filters["velocity_max"]):
                    match_filter = False

            if "velocity_min" in filters and "velocity_max" in filters:
                if approach.velocity < float(filters["velocity_min"]) or approach.velocity > float(filters["velocity_max"]):
                    match_filter = False

            if "diameter_min" in filters and "diameter_max" not in filters:
                if math.isnan(approach.neo.diameter) is True or approach.neo.diameter < float(filters["diameter_min"]):
                    match_filter = False

            if "diameter_min" not in filters and "diameter_max" in filters:
                if math.isnan(approach.neo.diameter) is True or approach.neo.diameter > float(filters["diameter_max"]):
                    match_filter = False

            if "diameter_min" in filters and "diameter_max" in filters:
                if math.isnan(approach.neo.diameter) is True or (approach.neo.diameter < float(filters["diameter_min"]) or approach.neo.diameter > float(filters["diameter_max"])):
                    match_filter = False

            if "hazardous" in filters:
                if filters["hazardous"] is False and approach.neo.hazardous is True:
                    match_filter = False

                if filters["hazardous"] is True and approach.neo.hazardous is False:
                    match_filter = False

            if match_filter is True:
                yield approach                
