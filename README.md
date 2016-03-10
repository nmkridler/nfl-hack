# NFL Hackathon - Pyxley App

This repository contains code that was used for the NFL Hackathon. The
data provided in this repository are __synthetic__ and __not the data that
was provided at the hackathon by the NFL__. This repository is purely meant
to demonstrate a basic application that leverages Blueprints and can
be extended to a larger application.

Check out Pyxley [here](https://github.com/stitchfix/pyxley)

## Installing Dependencies
Install NPM. Then run `npm install`. Alternatively, running
`pyxapp --init . ` will install all of the dependencies needed.


## Building
This repository has a prebuilt JavaScript bundle (`pyxleyapp\static\bundle.js`). If you wish to have python build the bundle, simply include the build option

`python run.py --build`

This will create the `ReactRouter` component and run Webpack to transpile
the jsx code.

## Running
After building the javascript bundle, type
```
python run.py
```
This should launch the app so that it is accessible on `localhost:5555`.

## What's In Here?
### Cached Data
Some of the dashboards I maintain are just pivots on simple reports that are
generated daily. Rather than manage a separate database, it's easier to just
load the data into memory. In `pyxleyapp/lib` we have two important
classes for handling the data: `Scheduler` and `CacheData`. `CacheData`
is a simple data manager that only reads CSV files, but can be modified
to read other data sources. `Scheduler` is a simple class that runs a function on a specified time interval. `CacheData` has methods for loading data
and for determining whether or not to try to load new data based on the
date.

In `run.py` we use these in the following way:

```python
from pyxleyapp.lib.scheduler import Scheduler
from pyxleyapp.lib.cache import CacheData
from pyxleyapp.models.config import FILES
cache = CacheData(FILES[args.env], env=args.env)
cache.load()

# The scheduler will run this function
def check_status():
    cache.status()
    for v in _views:
        if v == "feedback":
            continue
        _views[v].status()

if __name__ == "__main__":
    # Start the scheduler
    scheduler = Scheduler(1800, check_status)
    scheduler.start()
    app.run(host='0.0.0.0')
    scheduler.stop()

```

### Model
The data model used here is not a true "Model" in the MVC sense. Instead
it's just a way to organize and separate the data from the application.
So any methods related loading the data are handled by `pyxleyapp/models/main.py`. When the application or data grow too large,
then it should be relatively easy to swap this layer out for a
different data source.

In this application, the base class is the `CacheModel` which handles
the daily data load. The `MainModel` class just holds the specifics
for the data needed by the `Main` page.

### View
Because Pyxley handles most of the data routing, we don't really
have a true "Controller" layer. Instead, we have this hybrid
View/Controller where we create the `blueprint` and also some
additional view functions.

The `MainView` derives from the `MainModel` class so that it has
access to the data. This is where we could easily swap out some
sort of database layer.  In the code snippet below, we pass the
cache object to the base class and create a `Blueprint` that we
will use to set up the Pyxley bits.

```python
class MainView(MainModel):

    def __init__(self, cache, save=False):
        super(MainView, self).__init__(cache)

        self.mod = Blueprint("main", __name__)
        self.mod.add_url_rule("/", view_func=self.index)
```

#### Blueprints
We use Flask [`blueprints`](http://flask.pocoo.org/docs/0.10/blueprints/) to create separate pages within the app. In this application, there's only one
page, but adding new pages can be done by copying the pattern.

#### The Pyxley UI
As with the examples provided in the Pyxley repo, we
can create a UI using Pyxley components.

```python
def build_ui(self):
    # Specify the layout
    self.ui = UILayout(
        "FilterChart",
        "./jsx/SimpleChart",
        "component_id")

    # Create a slider
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

    # Save the file
    self.ui.render_layout(self.mod,
        self.static_ + "/layout.js",
        alias="Main")

    # Assign the routes
    self.ui.assign_routes(self.mod)
```

This function doesn't need to belong to the class, but for organizational
purposes, there's nothing really wrong with it being there.

### Custom JavaScript
This repository also includes some additional React components that don't exist in Pyxley. The point was to show how easy it is to use them when
bundling with Webpack. In the `build_ui` code above, you may have noticed
that the layout is pointing to `./jsx/SimpleChart`. This makes it easy
to add widgets that are specific to the application. 
