$(document).ready(function() {
    runAnimationSequence();
    initializeAddressSearch();

    $("#search-form, #address-search-form").submit(function(event) {
        start_loader();
    });
});


function runAnimationSequence() {
    $(".animation-group").velocity("transition.slideUpIn", {duration: 1200, stagger: 200})
}


function initializeAddressSearch() {
    let autocomplete = new google.maps.places.Autocomplete(document.getElementById("search-address"));
    autocomplete.setTypes(["address"]);
    autocomplete.addListener("place_changed", submitAddress);
}


function submitAddress() {
    $("#address-search-form").submit();
}


function start_loader() {
    $(".preloader-wrapper").addClass("active");
    $(".loading-text").fadeIn();
}
