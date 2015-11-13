import                              '../../bower_components/mixpanel/mixpanel-jslib-snippet';
import { default as $ } from        '../../bower_components/jquery/dist/jquery';

const W = window, D = W.document;
let ignore = false;

try {
    ignore = require('../../ignore.json').test;
} catch(e) {
    ignore = false;
}

// Check existing elements
const INPUTS = $('input:not([type=submit]):not([type=checkbox])'),
    VIEW_PLAYS_BUTTON = $('input[type=submit]'),
    SHOW_ALL_PLAYS_CHECKBOX = $('input[type=checkbox]'),
    QUARTERS = $('.quarter');

if (ignore === false) {

    // Init mixpanel
    mixpanel.init('0ba5f89c31ca2df1c18db354855ff043');

    if (VIEW_PLAYS_BUTTON.length) {
        VIEW_PLAYS_BUTTON.click(function() {
            const INPUT_VALUES = getAllInputValues();

            mixpanel.track('View Plays', {
                week: INPUT_VALUES.week,
                year: INPUT_VALUES.year,
                player: INPUT_VALUES.name
            });
        });
    }

    if (SHOW_ALL_PLAYS_CHECKBOX.length) {
        SHOW_ALL_PLAYS_CHECKBOX.click(function() {
            const INPUT_VALUES = getAllInputValues();

            mixpanel.track('Show All Plays', {
                week: INPUT_VALUES.week,
                year: INPUT_VALUES.year,
                player: INPUT_VALUES.name
            });
        });
    }

    if (QUARTERS.length) {
        QUARTERS.click(function(e) {
            const INPUT_VALUES = getAllInputValues(),
                QUARTER = $(this).closest('.quarter');

            mixpanel.track('Table Event', {
                week: INPUT_VALUES.week,
                year: INPUT_VALUES.year,
                player: INPUT_VALUES.name,
                quarter: QUARTER.attr('data-attr'),
                action: QUARTER.hasClass('collapsed') ? 'Expand' : 'Collapse'
            });
        });
    }
}

function getAllInputValues() {
    let obj = {};

    // Collect values from inputs indiscriminately
    INPUTS.each(function(i, v) {
        let val = v.value,
            numberVal = parseInt(val);
        obj[ v.name ] = !isNaN(numberVal) ? numberVal : val ? val : null;
    });

    return obj;
}

export default getAllInputValues;