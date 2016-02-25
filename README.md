# NFL Hackathon - Pyxley App

## Versions
This app currently depends on development versions of `pyxley` and `pyxleyJS`.
The development branches are called `webpack` and can be found at the
respective repositories.

It is recommended to work in a virtual environment using a tool like `virtualenv`
or `conda`.

## Installing Dependencies
```
npm install
```

If you have cloned the `pyxleyJS` webpack branch, set up a link. Go to the
directory of `pyxleyJS` and type:
```
npm link
```
This will create a virtual link. Go back to the directory for this app and
type
```
npm link pyxley
```
to install the symbolic link to the `pyxleyJS` version.


## Building
There is a `bundle.js` that has been prebuilt. However, if you wish to rebuild,
simply type
```
python build.py
```

This will create files that need to be transpiled using webpack.
```
node_modules/.bin/webpack
```
will build the necessary `bundle.js`.

## Running
After building the javascript bundle, type
```
python run.py
```
This should launch the app so that it is accessible on `localhost:5555`.
