$(function () {
    $('input.address').each(function () {
        var self = $(this);
        var cmps = $('#' + self.attr('name') + '_components');
        var fmtd = $('input[name="' + self.attr('name') + '_formatted"]');
        self.geocomplete({
            details: cmps,
            detailsAttribute: 'data-geo',
            autoselect: false,
            types: ["geocode", "establishment"],
            blur: true,
            map: ".data-geo-map"
        })
        .bind("geocode:result", function(event, result) {
            console.log("Result: " + result.formatted_address);
        })
        .bind("geocode:error", function(event, status){ 
            console.log("ERROR: " + status);
        })
        .bind("geocode:multiple", function(event, results) {
            console.log("Multiple: " + results.length + " results found");
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
