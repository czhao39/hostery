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
            }]
        }
    };

    let chart = new Chart(context, {
        type: "bar",
        data: data,
        options: options,
    });
}
