(function(w, d) {
    'use strict';

    $(d).ready(function() {
        $('form').submit(function(e) {
            e.preventDefault();

            var inputs = $('input'),
                obj = {};

            inputs.each(function(i, v) {
                obj[ v.name ] = parseInt(v.value) || null;
            });

            $.getJSON(
                './rushing_yds.json?inputYear=' + obj.year + '&inputWeek=' +
                obj.week,
                function(data) {
                    $('#result').html(data.slice(0, obj.limit).join('<br />'));
                }
            );
        });
    });
})(window, document);