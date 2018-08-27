$(function () {
    $('input.address').each(function () {
        var self = $(this);
        var cmps = $('#' + self.attr('name') + '_components');
        var fmtd = $('input[name="' + self.attr('name') + '_formatted"]');
        self.geocomplete({
            details: cmps, // The container that should be populated with data.
            detailsAttribute: 'data-geo', // The attribute's name to use as an indicator.
            autoselect: false, // Automatically selects the highlighted item or the first item from the suggestions list on Enter.
            types: ["geocode", "establishment"], // An array containing one or more of the supported types for the places request.
                                                 // Default: `['geocode']` See the full list [here]
                                                 // (http://code.google.com/apis/maps/documentation/javascript/places.html#place_search_requests)
            blur: true, // Trigger geocode when input loses focus.
            map: ".data-geo-map", // Might be a selector, an jQuery object or a DOM element.
            bounds: false, // Whether to snap geocode search to map bounds. Default: `true` if false search globally.
                           // Alternatively pass a custom `LatLngBounds object.
            geocodeAfterResult: false, // If blur is set to true, choose whether to geocode if user has explicitly selected a result before blur.
            restoreValueAfterBlur: false, // Restores the input's value upon blurring.
        })
        .bind("geocode:result", function(event, result) {
            console.log("single result: " + result.formatted_address);
            console.log(dir(result));
            // self.val(result.formatted_address);
        })
        .bind("geocode:error", function(event, status){ 
            console.log("ERROR: " + status);
        })
        .bind("geocode:multiple", function(event, results) {
            console.log("Multiple: " + results.length + " results found");
            results.forEach(function(result) {
                console.log("\tresult: " + result.formatted_address);
            });
        })
        .change(function () {
            if (self.val() != fmtd.val()) {
                var cmp_names = [
                    'country',
                    'country_code',
                    'locality',
                    'postal_code',
                    'route',
                    'street_number',
                    'state',
                    'state_code',
                    'formatted',
                    'latitude',
                    'longitude',
                ];
                for (var ii = 0; ii < cmp_names.length; ++ii) {
                    $('input[name="' + self.attr('name') + '_' + cmp_names[ii] + '"]').val('');
                }
            }
        });
    });
});
