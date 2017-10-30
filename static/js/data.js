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
