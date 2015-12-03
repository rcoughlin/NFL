import { default as $ } from        '../../bower_components/jquery/dist/jquery';
import { default as values } from   './mixpanel.es6';
import { default as grid } from     './components/grid.es6';

const W = window,
    D = W.document,
    PLAY_TOGGLE_CHECKBOX = $('input[name=toggle]'),
    QUARTERS = $('.quarter');
let playByPlay = W.location.pathname.indexOf('play') > -1,
    url = './' + (playByPlay ? 'plays_by_team' : 'rushing_yds') +
        '.json?',
    plays;

// Setup checkbox events, hide
PLAY_TOGGLE_CHECKBOX.click(e => {
    let nonPlayerPlays = $('.non-player');
    if ($(e.target)[0].checked === true) {
        nonPlayerPlays.show();
    } else {
        nonPlayerPlays.hide();
    }
});

QUARTERS.click(e => $(e.target).closest('.quarter').toggleClass('collapsed'));

$('form').submit(function(e) {
    e.preventDefault();

    let obj = values(),
        parameterizedUrl;

    parameterizedUrl = url + stringifyQueryParams(obj);
    $.getJSON(parameterizedUrl, function(data) {
        let result = $('#result'),
            err = '<div>No Results Found</div>';

        // If we get data back from our endpoints
        if (data && data.length) {

            // For team plays endpoint
            if (playByPlay) {
                grid(data);
            } else {

                // For root "yards" endpoint
                result.html(data.slice(0, obj.limit).join('<br />'));
            }
        } else {
            result.html(err);
        }
    });
});

function stringifyQueryParams(obj) {
    let str = '';

    for (let key in obj) {
        let value = obj[ key ];
        str += key + '=' + encodeURIComponent(value) + '&';
    }
    return str;
}