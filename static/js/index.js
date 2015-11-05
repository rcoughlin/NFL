(function(w, d) {
    'use strict';

    var playByPlay = w.location.pathname.indexOf('play') > -1,
        url = './' + (playByPlay > -1 ? 'plays_by_player' : 'rushing_yds') +
            '.json?';

    $(d).ready(function() {
        $('form').submit(function(e) {
            e.preventDefault();

            var inputs = $('input:not([type=submit])'),
                obj = {},
                parameterizedUrl;

            inputs.each(function(i, v) {
                var val = v.value,
                    numberVal = parseInt(val);
                obj[ v.name ] = !isNaN(numberVal) ? numberVal : val ? val : null;
            });

            parameterizedUrl = url + stringifyQueryParams(obj);
            $.getJSON(parameterizedUrl, function(data) {
                var html;

                console.log(data);

                if (playByPlay) {
                    html = data.map(function(v) {
                        return [ 'Q' + v.qtr, v.desc ].join(' ');
                    }).join('<br />');
                } else {
                    html = data.slice(0, obj.limit).join('<br />');
                }

                $('#result').html(html);
            });
        });

        function stringifyQueryParams(obj) {
            var str = '';

            for (var key in obj) {
                var value = obj[ key ];
                str += key + '=' + encodeURIComponent(value) + '&';
            }
            return str;
        }
    });
})(window, document);