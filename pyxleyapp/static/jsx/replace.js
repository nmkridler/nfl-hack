
import React from 'react';
import $ from 'jquery';

export class ReplaceImages extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: []
        };
    }

    _initAlerts(){
        $.get(this.props.url.concat("?",
            $.param(
                {
                    play_index: 1
                })
            ),
        function(r){
            this.setState({data: r.result});
        }.bind(this));
    }

    update(items) {
        let url = this.props.url.concat("?",$.param(items));
        $.get(url, function(r){
            this.setState({data: r.result});
        }.bind(this));

    }

    componentDidMount() {
        this._initAlerts();
    }

    render() {
        var header = this.state.data.map(function(item, index){
            return(
                <td>
                    <div className="SimInfo">
                        <h4><span className="pull-left label label-default">{item.position} {item.jersey}</span></h4>
                        <h4><span className="pull-right label label-default">{item.name}</span></h4>
                    </div>

                </td>

            );
        }.bind(this));
        var images = this.state.data.map(function(item, index){
            return(
                <td className="style-image-table">
                <img className="style-image" src={item.imgsrc} height="125"></img>
                <div className="Siminfo">
                     <h4><span className="pull-left label label-default">Score: {item.dist}</span></h4>
                </div>
                </td>

            );
        }.bind(this));


        return(
            <div className="bs-scroll">
            <table className="dash-grid" style={ { width: "100%" } }>
                <tbody>
                    <tr>
                    {header}
                    </tr>
                    <tr>
                    {images}
                    </tr>
                </tbody>
            </table>
            </div>
        );
    }
};
