import React from 'react';
import {Button, Row, Col} from 'react-bootstrap';
import {Filter, Chart} from 'pyxley';
import {ReplaceImages} from './replace.js';

export class FilterChart extends React.Component {
    constructor(props) {
        super(props);
    }

    _handleClick(input) {
        var params = {};
        for(var i = 0; i < this.props.filters.length; i++){
            var vals = this.refs["filter_".concat(i)].refs.filter.getCurrentState();
            for(var key in vals){
                params[key] = vals[key];
            }
        }
        if(input){
            for(var i = 0; i < input.length; i++){
                params[input[i].alias] = input[i].value;
            }
        }
        for(var i = 0; i < this.props.charts.length+1; i++){
            this.refs["chart_".concat(i)].update(params);
        }
        return params;
    }

    render() {
        var items = this.props.filters.map(function(x, index){
            return(<Filter
                key={"fkey_".concat(index)}
                ref={"filter_".concat(index)}
                onChange={this._handleClick.bind(this)}
                dynamic={this.props.dynamic}
                type={x.type} options={x.options}/>);
        }.bind(this));

        var charts = this.props.charts.map(function(x, index){
            if(x.type != "Random"){
                return(<Chart
                    ref={"chart_".concat(index)}
                    type={x.type} options={x.options}/>);
            }
        });

        var ncharts = this.props.charts.length;
        return (
            <div>
                <Row>
                <div className={this.props.filter_style}>
                {items}
                </div>
                </Row>
                <Row>


                <ReplaceImages
                    ref={"chart_".concat(ncharts)}
                    url={"/images/"} />
                </Row>
                <Row>
                {charts}
                </Row>

            </div>
        );
    }
}
