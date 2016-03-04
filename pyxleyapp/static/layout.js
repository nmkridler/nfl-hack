
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { FilterChart as Component} from './jsx/SimpleChart';

    var filter_style = "'btn-group'";
var dynamic = true;
var charts = [{"type": "PlotlyAPI", "options": {"chartid": "plotlyid", "url": "/plotlyurl/", "params": {"play_index": "1"}}}, {"type": "Random", "options": {"chartid": "imagechart", "url": "/images/"}}];
var filters = [{"type": "SliderInput", "options": {"min": 1, "default": "1", "max": 95, "label": "play_index", "alias": "play_index", "step": 1}}];

    class Main extends React.Component {
        constructor(props) {
            super(props);
        }

        render() {
            return (
                <Component { ...this.props } />
            );
        }
    }
    Main.defaultProps = {
        filter_style : filter_style,
dynamic : dynamic,
charts : charts,
filters : filters
    };
    export default Main;

    