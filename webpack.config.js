
        var path = require("path");
        var webpack = require("webpack");

        module.exports = {
          entry: [
              './pyxleyapp/static//index.js',
              './pyxleyapp/static/jsx/navbar.js'
          ],
          output: {
            path: path.join(__dirname,'./pyxleyapp/static/'),
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
                include: path.join(__dirname,'./pyxleyapp/static/'),
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
                new webpack.ProvidePlugin({
                  $: "jquery",
                  jQuery: "jquery"
                })
            ]
        };
