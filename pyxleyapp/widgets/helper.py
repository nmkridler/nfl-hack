
from pyxley.charts import Chart
from flask import jsonify, request
import numpy as np

class Images(Chart):
    imgs = {
        "home": [
            "cody1.jpg",
            "cody2.jpg",
            "cody3.jpg",
            "caylee1.jpg",
            "caylee2.jpg"
        ],
        "away": [
            "cody1.jpg",
            "cody2.jpg",
            "cody3.jpg",
            "caylee1.jpg",
            "caylee2.jpg"
        ]
    }
    def __init__(self, init_params, indata, outdata, route_func=None):

        options = {
            "chartid": "imagechart",
            "url": "/images/"
        }

        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            _in = self.apply_filters(indata, args)
            _out = self.apply_filters(outdata, args)

            return jsonify(Images.to_json(
                    _in, _out, self.imgs
                ))
        if not route_func:
            route_func = get_data
        super(Images, self).__init__("Random", options, route_func)

    @staticmethod
    def to_json(indata, outdata, imgs):
        _in = indata.sort_values(by="dist", ascending=False)

        useimgs = imgs["home"]
        _dir = "./static/"
        if "away" in _in.team.values:
            useimgs = imgs["away"]
            _dir = "./static/"

        np.random.shuffle(useimgs)

        out = []
        _pcount = 0
        _seen = {}
        for i, row in _in.iterrows():
            idx = outdata.position == row["position"]
            if idx.sum() == 0:
                continue
            _out = outdata[idx].sort_values(by="dist")
            if _out["displayName"].iloc[0] in _seen:
                continue

            out.append(
            {
                "name": _out["displayName"].iloc[0],
                "jersey": _out["jerseyNumber"].iloc[0],
                "dist": "%.2f"%_out["dist"].iloc[0],
                "imgsrc": _dir+useimgs[_pcount],
                "position": _out["position"].iloc[0]
            })
            _seen[ (_out["displayName"].iloc[0],
                    _out["jerseyNumber"].iloc[0])] = True
            _pcount += 1
            if _pcount == 5:
                break

        return {
            "result": out
        }


class PlotlyAPI(Chart):
    def __init__(self, options, route_func):
        super(PlotlyAPI, self).__init__("PlotlyAPI", options, route_func)

class PlotlyLines(PlotlyAPI):
    def __init__(self, xypairs, data_source,
        names=[],
        labels=[],
        mode="markers+text",
        ptype="scatter",layout={},
        init_params={},
        chart_id="plotlyid", url="/plotlyurl/",
        route_func=None):

        self.options = {
            "chartid": chart_id,
            "url": url,
            "params": init_params
        }
        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            df = self.apply_filters(data_source, args)
            return jsonify(PlotlyLines.to_json(
                    df,
                    xypairs,
                    mode,
                    ptype,
                    labels,
                    layout,
                    names
                ))
        if not route_func:
            route_func = get_data

        super(PlotlyLines, self).__init__(self.options, route_func)

    @staticmethod
    def to_json(df, xypairs, mode,
        ptype, labels, layout, names):
        _OFFENSE = {"TE", "WR", "RB", "G", "P", "OG", "QB", "FB", "C", "K"}

        if df.empty:
            return {
                "x": [],
                "y": [],
                "text": [],
                "mode": mode,
                "type": ptype
            }

        _data = []
        for pair, label, name in zip(xypairs, labels, names):
            x, y = pair
            _size = 24
            _color = 'rgb(93, 164, 214)'

            _marker = "x"
            if (x in df.columns) and (y in df.columns):
                players = set(df[label].values.tolist())
                if len(players.intersection(_OFFENSE)) > 2:
                    _usedist = "dist"
                    _color = 'rgb(255, 65, 54)'
                    _marker = "circle-open"
                    if name == "away":
                        _usedist = "dist_away"
                    _size = df[_usedist].values.tolist()

                _marker_data = {
                    "size": _size,
                    "symbol": _marker,
                    "color": _color,
                    "line": {"width": 4}
                }
                _data.append(
                    {
                        "x": df[x].values.tolist(),
                        "y": df[y].values.tolist(),
                        "text": df[label].values.tolist(),
                        "name": name,
                        "mode": mode,
                        "type": ptype,
                        "marker": _marker_data
                    }
                )

        return {
            "data": _data,
            "layout": layout
            }
