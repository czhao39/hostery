$(document).ready(function() {
    $("#search-form").submit(function(event) {
        start_preloader();
    })
});


function start_preloader() {
    $(".preloader-wrapper").addClass("active");
    $(".loading-text").fadeIn();
}
