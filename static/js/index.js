$(document).ready(function () {
    runAnimationSequence();

    $("#search-form").submit(function (event) {
        start_loader();
    });
});


function runAnimationSequence() {
    $(".animation-group").velocity("transition.slideUpIn", {duration: 1200, stagger: 200})
}

function start_loader() {
    $(".preloader-wrapper").addClass("active");
    $(".loading-text").fadeIn();
}
