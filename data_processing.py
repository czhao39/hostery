import csv

import heapq
from collections import defaultdict
import numpy as np


# Set this to False in production!!
DEV = False
if DEV:
    import matplotlib.pyplot as plt


PRIMARY_COLOR = "rgba(33, 150, 243, 0.5)"
ACCENT_COLOR = "rgba(255, 109, 0, 0.5)"

# Load listings into memory
LISTINGS_PATH = "airbnb-sep-2017/listings.csv"
with open(LISTINGS_PATH) as listings_csv:
    listings = [listing for listing in csv.DictReader(listings_csv)]


def get_dist_squared(lat1, lng1, lat2, lng2):
    return (lat1 - lat2) ** 2 + (lng1 - lng2) ** 2


def price_str_to_float(price_str):
    return float(price_str[1:].replace(',', ''))


def round_to(num, dec_places):
    return round(num * 10 ** dec_places) / (10 ** dec_places)


def get_closest_listing(lat, lng):
    """
    Returns the closest listing with a defined neighborhood given a latitude (lat) and longitude (lng).
    """

    return min((listing for listing in listings if listing["host_neighbourhood"]),
               key=lambda l: get_dist_squared(lat, lng, float(l["latitude"]), float(l["longitude"])))


def get_weekly_avg_income(lat, lng, n=5):
    """
    Given the latitude (lat) and longitude (lng) of a new listing, estimates the average weekly income per hostee by using data from the n closest listings.
    """

    listings_by_dist = []
    for listing in listings:
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        price = price_str_to_float(listing["price"])
        availability = float(listing["availability_30"])
        # The estimated probability of the listing being booked on any given night, assuming that the actual availability will be approximately half of the availability over the next 30 days
        booking_ratio = (30 - availability / 2) / 30
        listings_by_dist.append((dist_sq, price, booking_ratio))
    n_closest = heapq.nsmallest(n, listings_by_dist)

    return sum(listing[1] * listing[2] for listing in n_closest) / n * 7


def get_optimal_price(lat, lng, n=30):
    """
    Given the latitude (lat) and longitude (lng) of a listing, estimates the nightly price that will maximize profits by using data from the n closest listings.
    """

    listings_by_dist = []
    for listing in listings:
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        price = price_str_to_float(listing["price"])
        availability = float(listing["availability_30"])
        # The estimated probability of the listing being booked on any given night, assuming that the actual availability will be approximately half of the availability over the next 30 days
        booking_ratio = (30 - availability / 2) / 30
        listings_by_dist.append((dist_sq, price, booking_ratio))
    n_closest = heapq.nsmallest(n, listings_by_dist)

    # Fit a quadratic to the income vs. price data, and determine the optimal price by finding the max of this curve
    prices = np.array([listing[1] for listing in n_closest])
    incomes = np.array([listing[1] * listing[2] for listing in n_closest])
    curve_coeffs = np.polyfit(prices, incomes, deg=2)

    if DEV:
        print("a = {}".format(curve_coeffs[0]))
        # Plot the income vs. price graph and approximation
        p = np.poly1d(curve_coeffs)
        xp = np.linspace(0, 1200, 100)
        plt.plot(prices, incomes, '.', xp, p(xp), '-')
        plt.ylim(0, 1000)
        plt.show()

    if curve_coeffs[0] > 0:
        # The income vs. price curve curves upwards, so there's no max! Just return the price of the listing associated with the highest income.
        return prices[max(range(n), key=lambda i: incomes[i])]

    # Vertex of the parabola is at x = -b / 2a
    return -curve_coeffs[1] / (2 * curve_coeffs[0])


def get_most_popular_neighborhood(min_ratings=20):
    """
    Returns the neighborhood with the most positive average rating, with at least min_ratings ratings.
    """

    # A dictionary mapping each neighborhood to [num_listings, total_rating]
    # Used for computing averages
    neighborhood_data = defaultdict(lambda: [0, 0])
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        rating = listing["review_scores_rating"]
        if not neighborhood or not rating:
            continue
        neighborhood_data[neighborhood][0] += 1
        neighborhood_data[neighborhood][1] += float(rating)

    neighborhood_avg_ratings = {n: neighborhood_data[n][1] / neighborhood_data[n][0] for n in neighborhood_data if
                                neighborhood_data[n][0] >= min_ratings}

    return max(neighborhood_avg_ratings, key=lambda n: neighborhood_avg_ratings[n])


def get_best_neighborhood_investment():
    """
    Returns the best neighborhood to invest in based on average nightly price and monthly number of ratings.
    """

    # A dictionary mapping each neighborhood to [num_listings, total_price]
    neighborhood_avg_price_data = defaultdict(lambda: [0, 0])
    # A dictionary mapping each neighborhood to its total number of reviews per month
    neighborhood_total_reviews = defaultdict(lambda: 0)
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        num_reviews = listing["reviews_per_month"]
        if not neighborhood or not num_reviews:
            continue
        neighborhood_avg_price_data[neighborhood][0] += 1
        neighborhood_avg_price_data[neighborhood][1] += price_str_to_float(listing["price"])
        neighborhood_total_reviews[neighborhood] += float(num_reviews)

    neighborhood_avg_prices = {n: neighborhood_avg_price_data[n][1] / neighborhood_avg_price_data[n][0] for n in
                               neighborhood_avg_price_data}
    # Investment score is proportional to average price and total number of reviews per month
    investment_scores = {n: neighborhood_avg_prices[n] * neighborhood_total_reviews[n] for n in neighborhood_avg_prices}

    return max(investment_scores, key=lambda n: investment_scores[n])


def get_neighborhood_avg_price(neighborhood, min_listings=4):
    """
    Returns the average price in neighborhood. If the number of listings in neighborhood is less than min_listings, returns None.
    """

    num_listings = 0
    total_price = 0
    for listing in listings:
        if listing["host_neighbourhood"] == neighborhood:
            num_listings += 1
            total_price += price_str_to_float(listing["price"])

    if num_listings < min_listings:
        return None

    return total_price / num_listings


def get_listing_avgs_data(query_neighborhood=None):
    """
    Returns the data object used by Chart.js to generate the Listing Averages radar chart for query_neighborhood if specified, or all neighborhoods if unspecified.
    """

    if not query_neighborhood:
        query_neighborhood = None

    METRICS = ["accommodates", "bathrooms", "bedrooms", "beds", "guests_included"]

    labels = [metric.replace('_', ' ').title() for metric in METRICS]
    data = []
    # A list where each item is a metric's [num_listings, total]
    # Used for computing averages
    metric_data = [[0, 0] for _ in METRICS]
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        if not neighborhood:
            continue
        if query_neighborhood is not None and neighborhood != query_neighborhood:
            continue
        for m in range(len(METRICS)):
            if len(listing[METRICS[m]]) == 0:
                continue
            metric_data[m][0] += 1
            metric_data[m][1] += float(listing[METRICS[m]])
    data = [round_to(metric[1] / metric[0], 2) if metric[0] > 0 else 0 for metric in metric_data]

    return {
        "labels": labels,
        "datasets": [{
            "data": data,
            "pointRadius": 5,
            "pointHoverRadius": 10,
            "pointHitRadius": 15,
            "pointBackgroundColor": ACCENT_COLOR,
            "backgroundColor": PRIMARY_COLOR,
        }],
    }


def get_price_vs_neighborhood_data(query_neighborhood=None, num_neighborhoods=8):
    """
    Returns the data object used by Chart.js to generate an Average Price vs. Neighborhood bar chart for the num_neighborhoods most popular neighborhoods, including query_neighborhood if specified.
    """

    if not query_neighborhood:
        query_neighborhood = None

    # A dictionary mapping each neighborhood to [num_listings, total_price]
    # Used for computing averages
    neighborhood_data = defaultdict(lambda: [0, 0])
    query_neighborhood_data = [0, 0]
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        if not neighborhood:
            continue
        if neighborhood == query_neighborhood:
            query_neighborhood_data[0] += 1
            query_neighborhood_data[1] += price_str_to_float(listing["price"])
        else:
            neighborhood_data[neighborhood][0] += 1
            neighborhood_data[neighborhood][1] += price_str_to_float(listing["price"])

    if query_neighborhood is None or query_neighborhood_data[0] == 0:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods, neighborhood_data,
                                               key=lambda n: neighborhood_data[n][0])
        chart_color = PRIMARY_COLOR
    else:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods - 1, neighborhood_data,
                                               key=lambda n: neighborhood_data[n][0])
        popular_neighborhoods.append(query_neighborhood)
        neighborhood_data[query_neighborhood] = query_neighborhood_data
        chart_color = [PRIMARY_COLOR] * (num_neighborhoods - 1)
        # Have the query neighborhood be an accent color
        chart_color.append(ACCENT_COLOR)

    labels = [neighborhood for neighborhood in popular_neighborhoods]
    data = [round_to(neighborhood_data[neighborhood][1] / neighborhood_data[neighborhood][0], 2) for neighborhood in
            popular_neighborhoods]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Average Price ($)",
            "data": data,
            "backgroundColor": chart_color,
        }],
    }


def get_listings_per_neighborhood_data(query_neighborhood=None, num_neighborhoods=8):
    """
    Returns the data object used by Chart.js to generate a Number of Listings per Neighborhood doughnut chart for the num_neighborhoods most popular neighborhoods, including the query_neighborhood if specified.
    """

    if not query_neighborhood:
        query_neighborhood = None

    # A dictionary mapping each neighborhood to the number of listings in that neighborhood
    neighborhood_counts = defaultdict(lambda: 0)
    query_neighborhood_count = 0
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        if not neighborhood:
            continue
        if neighborhood == query_neighborhood:
            query_neighborhood_count += 1
        else:
            neighborhood_counts[neighborhood] += 1

    if query_neighborhood is None or query_neighborhood_count == 0:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods, neighborhood_counts, key=neighborhood_counts.get)
        chart_color = PRIMARY_COLOR
    else:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods - 1, neighborhood_counts, key=neighborhood_counts.get)
        popular_neighborhoods.append(query_neighborhood)
        neighborhood_counts[query_neighborhood] = query_neighborhood_count
        chart_color = [PRIMARY_COLOR] * (num_neighborhoods - 1)
        # Have the query neighborhood be an accent color
        chart_color.append(ACCENT_COLOR)

    labels = [neighborhood for neighborhood in popular_neighborhoods]
    data = [neighborhood_counts[neighborhood] for neighborhood in popular_neighborhoods]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Number of Listings",
            "data": data,
            "backgroundColor": chart_color,
        }],
    }


def get_price_distribution_data(query_neighborhood=None, interval_size=50):
    """
    Returns the data object used by Chart.js to generate a price distribution histogram for query_neighborhood if specified, or all neighborhoods if unspecified.
    """

    if not query_neighborhood:
        query_neighborhood = None

    # A dictionary mapping interval start points to frequencies
    distribution = defaultdict(lambda: 0)
    for listing in listings:
        if query_neighborhood is not None and listing["host_neighbourhood"] != query_neighborhood:
            continue
        interval_start = int(price_str_to_float(listing["price"]) // interval_size * interval_size)
        distribution[interval_start] += 1

    sorted_intervals = sorted(distribution.keys())
    labels = ["${}\u2013${}".format(interval_start, interval_start + interval_size - 1) for interval_start in
              sorted_intervals]
    data = [distribution[interval_start] for interval_start in sorted_intervals]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Number of Listings",
            "data": data,
            "backgroundColor": PRIMARY_COLOR,
        }],
    }


# For testing purposes.
if __name__ == "__main__":
    listing = get_closest_listing(37.7541839478958, -122.406513787399)
    print(listing.keys())
