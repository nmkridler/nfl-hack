var path = require("path");
var webpack = require("webpack");

var root = './pyxleyapp/static'

module.exports = {
  entry: [
      root+"/layout.js"
  ],
  output: {
    path: './pyxleyapp/static/',
    sourceMapFilename: 'bundle.map',
    filename: 'bundle.js'
  },
  resolve: {
      extensions: ['', '.js', '.scss'],
      alias: {
          react: path.resolve('./node_modules/react')
      }
  },

  module: {
    loaders: [
      {
        test: /\.js?$/,
        include: path.join(__dirname, './pyxleyapp/static/'),
        loader: ['babel-loader'],
        exclude: /node_modules/,
        query: {
            presets: ['es2015', 'react']
        }
      },
      {
        test: /\.scss$/,
        loaders: ['style', 'css', 'sass']
      },
      {
        test: /\.json$/,
        loader: 'json'
      }
    ]
},
plugins: [

        // new webpack.optimize.UglifyJsPlugin(),
        // new webpack.optimize.DedupePlugin(),
        // new webpack.DefinePlugin({
        //     "process.env": {
        //         NODE_ENV: '"production"'
        //     }
        // }),
        new webpack.ProvidePlugin({
          $: "jquery",
          jQuery: "jquery"
        })
        // new webpack.NoErrorsPlugin()

    ]
};
