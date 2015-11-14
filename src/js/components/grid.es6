import React, { Component } from            '../../../bower_components/react/react-with-addons';
import { default as $ } from                '../../../bower_components/jquery/dist/jquery';

// TODO Refactor the way this adds to the page
const QUARTERS = $('.quarter'),
    PLAYER_NAME_INPUT = $('input[name=name]');

class PlayRow extends Component {
    render() {
        const row = this.props.row;
        return <tr className={this.props.row.hasPlayer ? '' : 'non-player'}>
            {Object.keys(row).filter(filterKeys).map((v, i) => {
                const val = row.hasOwnProperty(v) ? row[ v ] : '';
                return <td key={i}>{val}</td>;
            })}
        </tr>;
    }
}

class PlayTable extends Component {
    render() {
        const data = this.props.data;
        return <span>
            <div className='table-header'>Quarter {data[ 0 ].qtr}</div>
            <div className='table-container'>
                <table>
                    <thead>
                        <tr>
                            {Object.keys(data[ 0 ]).filter(filterKeys).map(
                                (v, i) => <th key={i}>{v}</th>
                            )}
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((v, i) => <PlayRow key={i} row={v} />)}
                    </tbody>
                </table>
            </div>
        </span>;
    }
}

function createQuarters(data) {
    let playObj = {},
        targetPlayer = PLAYER_NAME_INPUT.val().split(' ');
    targetPlayer = `${
        targetPlayer[ 0 ].charAt(0)
    }.${
        targetPlayer.pop()
    }`;

    // Loop over the plays, adding a reference to our obj for each one.
    // Filter is no good
    data.forEach(v => {
        let qtr = v.qtr;

        v.hasPlayer = getPlayersFromPlayData(v).indexOf(targetPlayer) > -1;

        if (!playObj.hasOwnProperty(qtr)) {
            playObj[ qtr ] = [];
        }

        playObj[ qtr ].push(v);
    });

    QUARTERS.each((i, v) => {
        let rows = playObj[ i + 1 ];
        React.render(<PlayTable data={rows} />, v);
    });
}

function getPlayersFromPlayData(play) {
    let players = [];

    for (let key in play.players || {}) {
        let value = play.players[ key ];

        players = players.concat(value.map(v => v.playerName));
    }

    return players;
}

function filterKeys(v) {
    return ['time', 'desc', 'down'].indexOf(v) > -1;
}

export default createQuarters;