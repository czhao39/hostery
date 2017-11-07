/*
 * Functions for creating the charts.
 */


// The Chart objects.
var listing_avgs_chart;
var listings_per_neighborhood_chart;
var price_distribution_chart;
var price_vs_neigborhood_chart;


// The selectors of the Chart canvases.
var listing_avgs_chart_selector;
var listings_per_neighborhood_chart_selector;
var price_distribution_chart_selector;
var price_vs_neigborhood_chart_selector;


/*
 * Add chart animation on scroll into viewport.
 *
 * @return {void}
 */
function initialize_scrollfire() {
    let options = [
        { selector: listing_avgs_chart_selector, offset: 50, callback: function() { listing_avgs_chart.render() } },
        { selector: listings_per_neighborhood_chart_selector, offset: 50, callback: function() { listings_per_neighborhood_chart.render() } },
        { selector: price_distribution_chart_selector, offset: 50, callback: function() { price_distribution_chart.render() } },
        { selector: price_vs_neigborhood_chart_selector, offset: 50, callback: function() { price_vs_neigborhood_chart.render() } },
    ];

    Materialize.scrollFire(options);
}


/*
 * Create the Listing Averages radar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_listing_avgs_chart(context, data) {
    listing_avgs_chart_selector = "#" + context;
    $context = $(listing_avgs_chart_selector);

    let options = {
        legend: {
            display: false
        },
        scale: {
            ticks: {
                min: 0,
                stepSize: 1
            }
        },
    };

    listing_avgs_chart = new Chart($context, {
        type: "radar",
        data: data,
        options: options,
    });

    listing_avgs_chart.resize();
    listing_avgs_chart.stop();
}


/*
 * Create the Listings per Neighborhood doughnut chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_listings_per_neighborhood_chart(context, data) {
    listings_per_neighborhood_chart_selector = "#" + context;
    $context = $(listings_per_neighborhood_chart_selector);

    let options = {
        legend: {
            display: false
        },
    };

    listings_per_neighborhood_chart = new Chart(context, {
        type: "doughnut",
        data: data,
        options: options,
    });

    listings_per_neighborhood_chart.resize();
    listings_per_neighborhood_chart.stop();
}

/*
 * Create the Price Distribution histogram
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_distribution_chart(context, data) {
    price_distribution_chart_selector = "#" + context;
    $context = $(price_distribution_chart_selector);

    let options = {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                barPercentage: 1.0,
                categoryPercentage: 1.0,
            }],
        },
    };

    price_distribution_chart = new Chart(context, {
        type: "bar",
        data: data,
        options: options,
    });

    price_distribution_chart.resize();
    price_distribution_chart.stop();
}

/*
 * Create the Average Price vs. Neighborhood bar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_vs_neighborhood_chart(context, data) {
    price_vs_neigborhood_chart_selector = "#" + context;
    $context = $(price_vs_neigborhood_chart_selector);

    let options = {
        scales: {
            xAxes: [{
                ticks: {
                    autoSkip: false
                }
            }],
            yAxes: [{
                ticks: {
                    // Prepend a dollar sign in the ticks
                    callback: function (value, index, values) {
                        return '$' + value;
                    }
                }
            }]
        },
        legend: {
            display: false
        },
    };

    price_vs_neigborhood_chart = new Chart(context, {
        type: "bar",
        data: data,
        options: options,
    });

    price_vs_neigborhood_chart.resize();
    price_vs_neigborhood_chart.stop();
}
