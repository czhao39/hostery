/*
 * Create the neighborhood radar chart
 */
function create_neighborhood_chart(data) {
    let context = $("#neighborhood_chart");

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
 * Create the listings per neighborhood doughnut chart
 */
function create_listings_per_neighborhood_chart(data) {
    let context = $("#listings_per_neighborhood_chart");

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
 */
function create_price_distribution_chart(data) {
    let context = $("#price_distribution_chart");

    let options = {
        legend: {
            display: false
        },
        title: {
            display: true,
            text: "Price Distribution",
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
