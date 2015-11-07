(function(w, d) {
    'use strict';

    let playByPlay = w.location.pathname.indexOf('play') > -1,
        url = './' + (playByPlay ? 'plays_by_team' : 'rushing_yds') +
            '.json?';

    $(d).ready(function() {
        const inputs = $('input:not([type=submit]):not([type=checkbox])'),
            playToggleCheckbox = $('input[name=toggle]'),
            playToggleParent = playToggleCheckbox.parent();
        let plays;

        // Setup checkbox events, hide
        playToggleCheckbox.click(function(e) {
            if (plays) {
                plays.toggle();
            }
        }).parent().hide();

        $('form').submit(function(e) {
            e.preventDefault();

            let obj = {},
                parameterizedUrl;

            // Collect values from inputs indiscriminately
            inputs.each(function(i, v) {
                let val = v.value,
                    numberVal = parseInt(val);
                obj[ v.name ] = !isNaN(numberVal) ? numberVal : val ? val : null;
            });

            parameterizedUrl = url + stringifyQueryParams(obj);
            $.getJSON(parameterizedUrl, function(data) {
                let result = $('#result'),
                    err = '<div>No Results Found</div>';

                // If we get data back from our endpoints
                if (data && data.length) {

                    // For team plays endpoint
                    if (playByPlay) {
                        let html = '';

                        // Loop through data, find associated players, build html
                        $(data).each((i, v) => {
                            const players = getPlayersFromPlayData(v),
                                player = `${
                                    obj.name.split(' ')[ 0 ].charAt(0)
                                }.${
                                    obj.name.split(' ').pop()
                                }`;

                            html += `
                                <div class="play ${
                                    players.indexOf(player) > -1 ? 'bold' : ''
                                }">
                                    Q${v.qtr} ${v.desc}
                                </div>
                            `;
                        });

                        // Collect regular (non player) plays and set html
                        plays = result.html(
                            html.replace(/\s{2,}/g, '')
                        ).find(':not(.bold)').hide();

                        // Iff there is html and it is not our error, show
                        // the checkbox, set to false
                        if (html) {
                            playToggleCheckbox.attr(
                                'checked', false
                            ).parent().show();
                        } else {
                            playToggleParent.hide();
                        }
                    } else {

                        // For root "yards" endpoint
                        result.html(data.slice(0, obj.limit).join('<br />'));
                    }
                } else {
                    playToggleParent.hide();
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

        function getPlayersFromPlayData(play) {
            let players = [];

            for (let key in play.players || {}) {
                let value = play.players[ key ];

                players = players.concat(value.map(v => v.playerName));
            }

            return players;
        }
    });
})(window, document);