from ..lib.cache import etl_date

class CacheModel(object):
    def __init__(self, cache, files):
        self.cache = cache
        self.files = files

    def _get_dates(self):
        self.etl_dates = {}
        _date = etl_date()
        for f in self.files:
            self.etl_dates[f] = _date

    def status(self):
        _status = [False]
        for f in self.files:
            if self.cache.etl_dates[f] != self.etl_dates[f]:
                _status.append(True)
                self.etl_dates[f] = self.cache.etl_dates[f]
                print "will reload %s" % f

        if any(_status):
            print "reload"
            self.load()


class MainModel(CacheModel):
    _FILES = ["locations", "on_field", "off_field"]
    def __init__(self, cache):

        super(MainModel, self).__init__(cache, self._FILES)
        self._get_dates()
        self.load()

    def load(self):
        self.on_field = self.cache.data["on_field"].copy()
        self.off_field = self.cache.data["off_field"].copy()
        self.locations = self.cache.data["locations"].copy()
