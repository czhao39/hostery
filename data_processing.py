import sys
import heapq
import csv


LISTINGS_PATH = "airbnb-sep-2017/listings.csv"
with open(LISTINGS_PATH) as listings_csv:
    listings = [listing for listing in csv.DictReader(listings_csv)]


def get_dist_squared(lat1, lng1, lat2, lng2):
    return (lat1 - lat2)**2 + (lng1 - lng2)**2


def price_str_to_float(price_str):
    return float(price_str[1:].replace(',', ''))


"""
Returns a listing object given a latitude (lat) and longitude (lng).
"""
def get_closest_listing(lat, lng):
    return min(listings, key=lambda l: get_dist_squared(lat, lng, float(l["latitude"]), float(l["longitude"])))


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
Returns the average price in the given neighborhood.
"""
def get_neighborhood_avg_price(neighborhood, min_listings=4):
    num_listings = 0
    total_price = 0
    for listing in listings:
        if listing["host_neighbourhood"] == neighborhood:
            num_listings += 1
            total_price += price_str_to_float(listing["price"])

    if num_listings < min_listings:
        return None

    return total_price / num_listings


"""
Returns the data array used by Chart.js to generate an Average Price vs. Neighborhood bar chart for the num_neighborhoods most popular neighborhoods.
"""
def get_price_vs_neighborhood_data(num_neighborhoods=10):
    # A dictionary mapping each neighborhood to [num_listings, total_price]
    neighborhood_data = {}
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        if not neighborhood:
            continue
        if neighborhood not in neighborhood_data:
            neighborhood_data[neighborhood] = [1, price_str_to_float(listing["price"])]
        else:
            neighborhood_data[neighborhood][0] += 1
            neighborhood_data[neighborhood][1] += price_str_to_float(listing["price"])

    popular_neighborhoods = heapq.nlargest(num_neighborhoods, neighborhood_data, key=lambda n: neighborhood_data[n][0])

    labels = []
    data = []
    for neighborhood in popular_neighborhoods:
        avg_price = neighborhood_data[neighborhood][1] / neighborhood_data[neighborhood][0]
        avg_price = round(avg_price * 100) / 100
        labels.append(neighborhood)
        data.append(avg_price)
    return {
            "labels": labels,
            "datasets": [{
                "label": "Average Price ($)",
                "data": data,
                "backgroundColor": "rgba(33, 150, 243, 0.5)",
                }],
            }


"""
For testing purposes.
"""
if __name__ == "__main__":
    listing = get_listing(37.7541839478958, -122.406513787399)
    print(listing.keys())
