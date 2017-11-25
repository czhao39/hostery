# Hostery | Maximize Your Airbnb Income


Setup
------
1. Clone this repo.
2. Create a Python 3 virtualenv called `venv` in the root of the project, and run `pip install -r requirements.txt`.
3. (optional) If you want to see a visualization of the profit optimization, install matplotlib and set `DEV = True` in `data_processing.py`.
4. Copy `secret.py.example` to `secret.py`. Obtain the required API keys and update `secret.py`.
5. Start the development server by running `run_dev_server.sh`.


Technologies Used
-----------------
* [Flask](http://flask.pocoo.org/)
* [Materialize](http://materializecss.com/)
* [Chart.js](http://www.chartjs.org/)
* [Google Maps APIs](https://developers.google.com/maps/)
* [NumPy](http://www.numpy.org/)
* [Heroku](https://www.heroku.com/)


Description
-----------
The Hostery was build with Flask in the backend and Materialize in the frontend. There are four main pages:
* Search: This is the home page, which allows the user to search by inputting coordinates or an address. I perform geocoding by using the Google Maps Geocode API.
* Data: This provides insights and  interactive charts ("Hostery SmartCharts") for the given neighborhood. It also shows summaries of nearby listings for hosts to compare their properties to.
* Overall Analytics: This is similar to the Data page, except it provides insights and charts for all of San Francisco.
* Help: This gives a brief description of each of the Hostery SmartCharts and how to use them.

All the data processing happens in `data_processing.py`. Here are several features:
* Visualize the data: The Data pages and Overall Analytics page show four Hostery SmartCharts, each described in the Help page.
* Price estimation: To estimate the average weekly income a homeowner can make with Airbnb, I assume that income is positively correlated with gross income. To estimate gross income, I multiply a listing's nightly price by its "bookings ratio," which is my estimate of the probability of the listing being booked for any given night. I average this estimated nightly income for the 5 closest listings and multiply by seven to get the weekly income.
* Bookings optimization: To maximize profits, I first get price vs. estimated income (see above for how I calculate estimated income) data for the 30 closest listings. Using a principle similar to that of the Laffer Curve, I suppose that the correlation between price and income is approximately quadratic, so I use NumPy to fit a quadratic to this data. I then find the vertex of this quadratic, which is the optimal price.
* Animate: I used Chart.js to create animated and interactive Hostery SmartCharts.
* Investment: To determine the best neighborhood to invest in, I assign each neighborhood an "investment score," which is equal to the neighborhood's average price times the neighborhood's total number of monthly ratings. I assume that the neighborhood's total number of monthly ratings is directly proportional to the demand in that neighborhood.
* Popularity: To determine the most popular neighborhood, I find the neighborhood with the highest average rating with at least 20 ratings.

The website is responsive, so it should look good on all screen sizes.
