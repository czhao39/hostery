/*
 * Functions for creating the charts.
 */


/*
 * Create the Neighborhood Averages radar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_neighborhood_chart(context, data) {
    $context = $("#" + context);

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

    let chart = new Chart($context, {
        type: "radar",
        data: data,
        options: options,
    });

    chart.resize();
}


/*
 * Create the Listings per Neighborhood doughnut chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_listings_per_neighborhood_chart(context, data) {
    $context = $("#" + context);

    let options = {
        legend: {
            display: false
        },
    };

    let chart = new Chart(context, {
        type: "doughnut",
        data: data,
        options: options,
    });

    chart.resize();
}

/*
 * Create the Price Distribution histogram
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_distribution_chart(context, data) {
    $context = $("#" + context);

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
        data: data,
        options: options,
    });

    chart.resize();
}

/*
 * Create the Average Price vs. Neighborhood bar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_vs_neighborhood_chart(context, data) {
    $context = $("#" + context);

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
                    callback: function(value, index, values) {
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
        data: data,
        options: options,
    });

    chart.resize();
}
