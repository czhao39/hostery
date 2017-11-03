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
        title: {
            display: true,
            text: "Neighborhood Averages",
            fontSize: 28,
            fontStyle: "normal"
        },
    };

    let chart = new Chart(context, {
        type: "radar",
        data: data,
        options: options,
    });
}


/*
 * Create the Listings per Neighborhood doughnut chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_listings_per_neighborhood_chart(context, data) {
    let options = {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: "Number of Listings per Neighborhood",
            fontSize: 28,
            fontStyle: "normal"
        },
    };

    let chart = new Chart(context, {
        type: "doughnut",
        data: data,
        options: options,
    });
}

/*
 * Create the Price Distribution histogram
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_distribution_chart(context, data) {
    let options = {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: "Neighborhood Price Distribution",
            fontSize: 28,
            fontStyle: "normal"
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
}

/*
 * Create the Average Price vs. Neighborhood bar chart
 *
 * @param {String} context
 * @param {Object} data
 * @return {void}
 */
function create_price_vs_neighborhood_chart(context, data) {
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
        title: {
            display: true,
            text: "Average Nightly Prices",
            fontSize: 28,
            fontStyle: "normal"
        }
    };

    let chart = new Chart(context, {
        type: "bar",
        data: data,
        options: options,
    });
}
