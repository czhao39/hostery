/*
 * Create the Average Price vs. Neighborhood bar chart
 */
function create_price_vs_neighborhood_chart(data) {
    let context = $("#price_vs_neighborhood_chart");

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
            text: "Average Prices in Most Popular Neighborhoods",
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
