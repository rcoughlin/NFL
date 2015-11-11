import React, { Component } from            '../../../bower_components/react/react-with-addons';
import { default as ReactDOM } from         '../../../bower_components/react-dom/react-dom';
import { default as $ } from                '../../../bower_components/jquery/dist/jquery';

const QUARTERS = $('.quarter');

class PlayRow extends Component {
    render() {
        const row = this.props.row;
        return <tr>
            {Object.keys(row).map((v, i) => {
                const val = JSON.stringify(row[ v ]);
                return <td key={i}>{val}</td>;
            })}
        </tr>;
    }
}

class PlayTable extends Component {
    render() {
        const data = this.props.data;
        return <table>
            <thead>
                <tr>
                    {Object.keys(data[ 0 ]).map((v, i) => <th key={i}>{v}</th>)}
                </tr>
            </thead>
            <tbody>
                {data.map((v, i) => <PlayRow key={i} row={v} />)}
            </tbody>
        </table>;
    }
}

function createQuarters(data) {
    QUARTERS.each((i, v) => {
        let rows = data.filter(v => v.qtr === i + 1);
        debugger;
        React.render(<PlayTable data={rows} />, v);
    });
}

export default createQuarters;