import sys
import heapq
import csv


# The tolerance allowed in assuming two coordinates are the same
COORD_TOLERANCE = 0.00001
LISTINGS_PATH = "airbnb-sep-2017/listings.csv"
with open(LISTINGS_PATH) as listings_csv:
    listings = [listing for listing in csv.DictReader(listings_csv)]


def get_dist_squared(lat1, lng1, lat2, lng2):
    return (lat1 - lat2)**2 + (lng1 - lng2)**2


def price_str_to_float(price_str):
    return float(price_str[1:].replace(',', ''))


"""
Returns a listing object given a latitude (lat) and longitude (lng).
Returns None if the listing is not found.
"""
def get_listing(lat, lng):
    for listing in listings:
        if abs(float(listing["latitude"]) - lat) < COORD_TOLERANCE and abs(float(listing["longitude"]) - lng) < COORD_TOLERANCE:
            return listing

    # Couldn't find a listing with the given coordinates
    return None


"""
Given the latitude and longitude of a new listing, estimates the average weekly income per hostee by averaging the prices of the n closest listings.
"""
def get_weekly_avg_income(lat, lng, n=4):
    listings_by_dist = []
    for listing in listings:
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        price = price_str_to_float(listing["price"])
        listings_by_dist.append((dist_sq, price))
    n_closest = heapq.nsmallest(n, listings_by_dist)

    return sum(listing[1] for listing in n_closest) / n * 7


"""
Given the latitude and longitude of a listingerty, estimates the nightly price that will maximize bookings by determining the lowest price within a distance of dist_range degrees.
"""
def get_max_bookings_price(lat, lng, dist_range=0.5):
    dist_range_sq = dist_range**2
    price_estimate = 1 << 32
    for listing in listings:
        price = price_str_to_float(listing["price"])
        if price >= price_estimate:
            continue
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        if dist_sq <= dist_range_sq:
            price_estimate = price

    # If no listings within dist_range away, return the price of the closest listing
    if price_estimate == 1 << 32:
        return get_weekly_avg_income(lat, lng, 1) / 7

    return price_estimate


"""
For testing purposes.
"""
if __name__ == "__main__":
    listing = get_listing(37.7541839478958, -122.406513787399)
    print(listing.keys())
