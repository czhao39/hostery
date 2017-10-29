import sys
import csv


LISTINGS_PATH = "airbnb-sep-2017/listings.csv"


"""
Returns a property object given a latitude (lat) and longitude (lng).
Returns None if the property is not found.
"""
def get_property(lat, lng):
    COORD_TOLERANCE = 0.00001  # the tolerance allowed in the latitude and longitude provided

    with open(LISTINGS_PATH) as listings_csv:
        listings = csv.DictReader(listings_csv)
        for prop in listings:
            if abs(float(prop["latitude"]) - lat) < COORD_TOLERANCE and abs(float(prop["longitude"]) - lng) < COORD_TOLERANCE:
                return prop

    # Couldn't find the property with the given coordinates
    return None


"""
For testing purposes.
"""
if __name__ == "__main__":
    prop = get_property(37.7541839478958, -122.406513787399)
    print(prop["beds"])
