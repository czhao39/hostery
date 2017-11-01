import csv

import heapq

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


def get_weekly_avg_income(lat, lng, n=4):
    """
    Given the latitude and longitude of a new listing, estimates the average weekly income per hostee by averaging the prices of the n closest listings.
    """

    listings_by_dist = []
    for listing in listings:
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        price = price_str_to_float(listing["price"])
        listings_by_dist.append((dist_sq, price))
    n_closest = heapq.nsmallest(n, listings_by_dist)

    return sum(listing[1] for listing in n_closest) / n * 7


def get_max_bookings_price(lat, lng, dist_range=0.5):
    """
    Given the latitude and longitude of a listingerty, estimates the nightly price that will maximize bookings by determining the lowest price within a distance of dist_range degrees.
    """

    dist_range_sq = dist_range ** 2
    price_estimate = 1 << 32
    for listing in listings:
        price = price_str_to_float(listing["price"])
        if not price or price >= price_estimate:
            continue
        dist_sq = get_dist_squared(lat, lng, float(listing["latitude"]), float(listing["longitude"]))
        if dist_sq <= dist_range_sq:
            price_estimate = price

    # If no listings within dist_range away, return the price of the closest listing
    if price_estimate == 1 << 32:
        return get_weekly_avg_income(lat, lng, 1) / 7

    return price_estimate


def get_neighborhood_avg_price(neighborhood, min_listings=4):
    """
    Returns the average price in the given neighborhood.
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


def get_neighborhood_metrics(neighborhood):
    """
    Returns the data object used by Chart.js to generate the Neighborhood Data radar chart for a given neighborhood.
    """

    METRICS = ["accommodates", "bathrooms", "bedrooms", "beds", "guests_included"]

    labels = [metric.replace('_', ' ').capitalize() for metric in METRICS]
    data = []
    # A list where each item is a metric's [num_listings, total]
    # Used for computing averages
    metric_data = [[0, 0] for _ in METRICS]
    for listing in listings:
        if listing["host_neighbourhood"] != neighborhood:
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
            "pointBackgroundColor": "rgba(41, 98, 255, 0.5)",
            "backgroundColor": "rgba(33, 150, 243, 0.5)",
        }],
    }


def get_price_vs_neighborhood_data(num_neighborhoods=10):
    """
    Returns the data object used by Chart.js to generate an Average Price vs. Neighborhood bar chart for the num_neighborhoods most popular neighborhoods.
    """

    # A dictionary mapping each neighborhood to [num_listings, total_price]
    # Used for computing averages
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

    labels = [neighborhood for neighborhood in popular_neighborhoods]
    data = [round_to(neighborhood_data[neighborhood][1] / neighborhood_data[neighborhood][0], 2) for neighborhood in
            popular_neighborhoods]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Average Price ($)",
            "data": data,
            "backgroundColor": "rgba(33, 150, 243, 0.5)",
        }],
    }


def get_listings_per_neighborhood_data(query_neighborhood=None, num_neighborhoods=8):
    """
    Returns the data object used by Chart.js to generate a Number of Listings per Neighborhood doughnut chart for the most popular neighborhoods, as well as the given neighborhood.
    """

    if len(query_neighborhood) == 0:
        query_neighborhood = None

    # A dictionary mapping each neighborhood to the number of listings in that neighborhood.
    neighborhood_counts = {}
    query_neighborhood_count = 0
    for listing in listings:
        neighborhood = listing["host_neighbourhood"]
        if not neighborhood:
            continue
        if neighborhood == query_neighborhood:
            query_neighborhood_count += 1
        elif neighborhood not in neighborhood_counts:
            neighborhood_counts[neighborhood] = 1
        else:
            neighborhood_counts[neighborhood] += 1

    if query_neighborhood is None or query_neighborhood_count == 0:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods, neighborhood_counts, key=neighborhood_counts.get)
        chart_color = "rgba(33, 150, 243, 0.5)"
    else:
        popular_neighborhoods = heapq.nlargest(num_neighborhoods - 1, neighborhood_counts, key=neighborhood_counts.get)
        popular_neighborhoods.append(query_neighborhood)
        neighborhood_counts[query_neighborhood] = query_neighborhood_count
        chart_color = ["rgba(33, 150, 243, 0.5)"] * (num_neighborhoods - 1)
        # Have the query neighborhood be an accent color
        chart_color.append("rgba(41, 98, 255, 0.5)")

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
    Returns the data object used by Chart.js to generate a price distribution histogram for the given query_neighborhood if specified, or all neighborhoods if unspecified.
    """

    if len(query_neighborhood) == 0:
        query_neighborhood = None

    # A dictionary mapping interval start points to frequencies
    distribution = {}
    for listing in listings:
        if query_neighborhood is not None and listing["host_neighbourhood"] != query_neighborhood:
            continue
        interval_start = int(price_str_to_float(listing["price"]) // interval_size * interval_size)
        if interval_start not in distribution:
            distribution[interval_start] = 1
        else:
            distribution[interval_start] += 1

    sorted_intervals = sorted(distribution.keys())
    labels = [u"${}\u2013${}".format(interval_start, interval_start + interval_size - 1) for interval_start in
              sorted_intervals]
    data = [distribution[interval_start] for interval_start in sorted_intervals]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Number of Listings",
            "data": data,
            "backgroundColor": "rgba(33, 150, 243, 0.5)",
        }],
    }


# For testing purposes.
if __name__ == "__main__":
    listing = get_closest_listing(37.7541839478958, -122.406513787399)
    print(listing.keys())
