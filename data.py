import sys
import heapq
import csv


LISTINGS_PATH = "airbnb-sep-2017/listings.csv"
# The tolerance allowed in assuming two coordinates are the same
COORD_TOLERANCE = 0.00001


def get_dist_squared(lat1, lng1, lat2, lng2):
    return (lat1 - lat2)**2 + (lng1 - lng2)**2


"""
Returns a property object given a latitude (lat) and longitude (lng).
Returns None if the property is not found.
"""
def get_property(lat, lng):
    with open(LISTINGS_PATH) as listings_csv:
        listings = csv.DictReader(listings_csv)
        for prop in listings:
            if abs(float(prop["latitude"]) - lat) < COORD_TOLERANCE and abs(float(prop["longitude"]) - lng) < COORD_TOLERANCE:
                return prop

    # Couldn't find the property with the given coordinates
    return None


"""
Given the latitude and longitude of a new property, estimates the weekly income per hostee by averaging the prices of the n closest properties.
"""
def estimate_weekly_income(lat, lng, n=4):
    props = []
    with open(LISTINGS_PATH) as listings_csv:
        listings = csv.DictReader(listings_csv)
        for prop in listings:
            dist_sq = get_distance_squared(lat, lng, float(prop["latitude"]), float(prop["longitude"]))
            price = float(prop["price"][1:])
            props.append((dist_sq, price))
    n_closest = heapq.nsmallest(n, props)

    return sum(prop[1] for prop in n_closest) / n * 7


"""
Given the latitude and longitude of a property, estimates the nightly price that will maximize bookings by determining the lowest price within a distance of dist_range degrees.
"""
def estimate_price_with_max_bookings(lat, lng, dist_range=0.5):
    dist_range_sq = dist_range**2
    props = []
    price_estimate = 1 << 32
    with open(LISTINGS_PATH) as listings_csv:
        listings = csv.DictReader(listings_csv)
        for prop in listings:
            if prop["price"] >= price_estimate:
                continue
            dist_sq = get_distance_squared(lat, lng, float(prop["latitude"]), float(prop["longitude"]))
            if dist_sq <= dist_range_sq:
                price_estimate = prop["price"]

    # If no properties within dist_range away, return the price of the closest property
    if price_estimate <= 0:
        return estimate_weekly_income(lat, lng, 1) / 7

    return price_estimate


"""
For testing purposes.
"""
if __name__ == "__main__":
    prop = get_property(37.7541839478958, -122.406513787399)
    print(prop.keys())
