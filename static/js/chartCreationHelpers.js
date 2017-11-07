/*
 * Functions for creating the charts.
 */


// Maps chart canvas selectors to Chart.js objects and datasets
var all_chart_info = new Map();


/*
 * Add chart animation on scroll into viewport.
 *
 * @return {void}
 */
function initialize_scrollfire() {
    let options = [];
    all_chart_info.forEach(function(val, key) {
        options.push({ selector: key, offset: 100, callback: function() {
            val.get("chart").data = val.get("data");
            val.get("chart").update();
        } });
    });

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
    let selector = "#" + context;
    all_chart_info.set(selector, new Map());
    all_chart_info.get(selector).set("data", data);

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

    let chart = new Chart(context, {
        type: "radar",
        options: options,
    });
    chart.resize();

    all_chart_info.get(selector).set("chart", chart);
}


/*
 * Create the Listings per Neighborhood doughnut chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_listings_per_neighborhood_chart(context, data) {
    let selector = "#" + context;
    all_chart_info.set(selector, new Map());
    all_chart_info.get(selector).set("data", data);

    let options = {
        legend: {
            display: false
        },
    };

    let chart = new Chart(context, {
        type: "doughnut",
        options: options,
    });
    chart.resize();

    all_chart_info.get(selector).set("chart", chart);
}

/*
 * Create the Price Distribution histogram
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_distribution_chart(context, data) {
    let selector = "#" + context;
    all_chart_info.set(selector, new Map());
    all_chart_info.get(selector).set("data", data);

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

    let chart = new Chart(context, {
        type: "bar",
        options: options,
    });
    chart.resize();

    all_chart_info.get(selector).set("chart", chart);
}

/*
 * Create the Average Price vs. Neighborhood bar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_vs_neighborhood_chart(context, data) {
    let selector = "#" + context;
    all_chart_info.set(selector, new Map());
    all_chart_info.get(selector).set("data", data);

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

    let chart = new Chart(context, {
        type: "bar",
        options: options,
    });
    chart.resize();

    all_chart_info.get(selector).set("chart", chart);
}
