# core modules
from __future__ import print_function
import os
import sys

# 3rd party modules
import googlemaps


class GoogleMaps(object):
    def __init__(self, key):
        self.gmaps = googlemaps.Client(key=os.environ['GOOGLE_KEY'])

    def calculate_distance(self, source, destination):
        """
        Return distance between 2 places in meters
        Return -1 if invalid
        """

        try:
            dist = -1
            directions_result = self.gmaps.distance_matrix(origins=[source],
                                                           destinations=[destination])
            if directions_result['status'] == 'OK':
                dist = directions_result['rows'][0]['elements'][0]['distance']['value']
            return dist
        except (NameError, KeyError) as e:
            print ("### Error fetching distance: {} {}".format(e.errno if hasattr(e, 'error') else "???",
                                                               e.strerror if hasattr(e, 'error') else e),
                   file=sys.stderr)
            return -1

    def get_lat_long(self, address):
        """
        Return lat long given an address
        :param address:
        :return:
        """
        try:
            ret = None
            geocode_result = self.gmaps.geocode(address=address)
            if geocode_result['status'] == 'OK':
                location = geocode_result[0]['geometry']['location']
                ret = (location['lat'], location['lng'])
            return ret
        except (NameError, KeyError) as e:
            print("### Error fetching distance: {} {}".format(e.errno if hasattr(e, 'error') else "???",
                                                              e.strerror if hasattr(e, 'error') else e),
                  file=sys.stderr)
            return None
