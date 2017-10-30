$(document).ready(function() {
    $("#search-form").submit(function(event) {
        start_loader();
    });
});


function start_loader() {
    $(".preloader-wrapper").addClass("active");
    $(".loading-text").fadeIn();
}
