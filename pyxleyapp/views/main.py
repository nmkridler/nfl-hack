from flask import render_template, make_response
from flask import request, jsonify
from flask import Blueprint
from . import config

from ..lib.factory import get_static_folder
from ..models.main import MainModel

from collections import OrderedDict
import pandas as pd
from pyxley.filters import SliderInput
from pyxley import UILayout
from ..widgets.helper import PlotlyLines, Images

from datetime import date
import time
import json
import logging

def add_plotly_chart(df, init_params, route_func=None):
    return PlotlyLines(
        [["y", "x"], ["y_away", "x_away"]],
        df,
        labels=["position", "position_away"],
        names=["Home", "Away"],
        init_params=init_params,
        layout={
            "hovermode": "closest",
            "plot_bgcolor": 'rgba(44,94,79,0.7)',
            "xaxis": {"range": [0, 53], "showgrid": False},
            "paper_bgcolor": 'rgba(44, 94, 79, 0.0)',
            "height": 600,
            "width": 1200
        },
        route_func=route_func)


def add_image_panel(on_field, off_field, init_params, route_func=None):
    return Images(init_params, on_field, off_field, route_func=route_func)

class MainView(MainModel):

    def __init__(self, cache, save=False):
        super(MainView, self).__init__(cache)

        self.mod = Blueprint("main", __name__)
        self.mod.add_url_rule("/", view_func=self.index)

        self.ins_, self.static_ = get_static_folder()

        self.init_params = {
            "play_index": "1"
        }

        self.build_ui(save)

    def index(self):

        return render_template('index.html',
            title="Main",
            base_scripts=config.JS,
            css=config.CSS,
            page_scripts=["bundle.js"])

    def build_ui(self, save):
        self.ui = UILayout(
            "FilterChart",
            "./jsx/SimpleChart",
            "component_id")


        sldr = SliderInput("play_index", 1,
            int(self.on_field["play_index"].max()),
            "play_index", "1")
        self.ui.add_filter(sldr)

        # Add a plotly chart
        self.ui.add_chart(
            add_plotly_chart(self.locations, self.init_params)
        )

        # Add the image panel
        self.ui.add_chart(
            add_image_panel(self.on_field, self.off_field,
                self.init_params)
        )

        if save:
            self.ui.render_layout(self.mod,
                self.static_ + "/layout.js",
                alias="Main")
        else:
            self.ui.assign_routes(self.mod)

    def check_args(self):
        args = {}
        for c in self.init_params:
            if request.args.get(c):
                args[c] = request.args[c]
            else:
                args[c] = self.init_params[c]
        return args

    def chart_data(self):
        args = self.check_args()
        df = PlotlyLines.apply_filters(
            self.locations, args)
        return jsonify(
            PlotlyLines.to_json(
                df,
                xypairs,
                mode,
                ptype,
                labels,
                layout,
                names
            ))

    def image_data(self):
        args = self.check_args()

        _in = Images.apply_filters(self.on_field, args)
        _out = Images.apply_filters(self.off_field, args)

        return jsonify(
            Images.to_json(
                _in, _out, Images.imgs
            ))
