import pandas as pd
import numpy as np
import json
import datetime
import logging

def parse_date(tokens):
    date = None
    for t in tokens:
        if "as_of" in t:
            date = datetime.datetime.strptime(t.split("=")[-1], "%Y%m%d").date()
    return date

def etl_date():
    today_ = datetime.date.today().toordinal()
    return datetime.date.fromordinal(today_).strftime("%Y%m%d")

def load_from_csv(filename, options):
    return pd.read_csv(filename, **options)

def load(filename, options={}, env="prod"):
    """ This could be changed to read from a database
    """
    return load_from_csv(filename, options)

def make_options(params, etl_date, env="local"):
    opts = { "name": params["name"] }
    opts["opts"] = {}
    if env == "prod":
        opts["opts"]["schema"] = params["schema"]
        if etl_date:
            opts["opts"]["partitions"] = [("as_of", etl_date)]
    return opts

class CacheData(object):
    """
    """
    def __init__(self, files, env="local"):
        """
            In this example, the env parameter won't matter,
            but it can be used to specify reading from a file
            or a database
        """
        self.files = files
        self.env = env
        self.data = {}
        self.etl_dates = self.get_dates()

    def get_dates(self):
        dates = {}
        for f in self.files:
            dates[f] = etl_date()
        return dates

    def load_file(self, params, filedate):
        dataframe = pd.DataFrame()
        opts = make_options(params,
                    filedate, env=self.env)
        try:
            dataframe = load(opts["name"],
                    opts["opts"], env=self.env)
        except:
            logging.warning("Failed to load %s"%opts["name"])
            return dataframe

        func = params["func"]
        if func:
            _data = func(dataframe)
        else:
            _data = dataframe

        return _data

    def set_data(self, name, filename, filedate):
        _data = self.load_file(filename, filedate)
        if not _data.empty:
            self.data[name] = _data
            self.etl_dates[name] = filedate

    def load(self):
        for f in self.files:
            print "loading {0}".format(f)
            self.set_data(f, self.files[f],
                self.etl_dates[f])

    def status(self):
        new_dates = self.get_dates()
        for f in self.files:
            if new_dates[f] != self.etl_dates[f]:
                self.set_data(f, self.files[f],
                    new_dates[f])
