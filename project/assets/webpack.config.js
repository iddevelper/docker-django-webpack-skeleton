'use strict';

var webpack = require('webpack');

var MiniCssExtractPlugin = require("mini-css-extract-plugin");
var Clean = require('clean-webpack-plugin');

module.exports = function (env) {
    env = env || {};

    var PRODUCTION = env.env == "production";
    
    var config = {
        mode: PRODUCTION ? 'production' : 'development',
        context: __dirname + '/frontend',
        entry: {
            main: './js/main',
            css_site: './sass/site'
        },

        output: {
            path: __dirname + '/dist/app',
            publicPath: '/static/app/',
            filename: 'js/[name].js'
        },

        resolve: {
            extensions: ['.js', '.scss'],
            modules: [__dirname + '/frontend', "node_modules"]
        },

        watch: !PRODUCTION,

        watchOptions: {
            aggregateTimeout: 300,
            poll: 500
        },

        optimization: {
            splitChunks: {
              cacheGroups: {
                styles: {
                  name: 'styles',
                  test: /\.(sa|sc|c)ss$/,
                  chunks: 'all',
                  enforce: true
                }
              }
            }
        },

        module: {
            rules: [
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        'css-loader',
                        'sass-loader',
                    ]
                },

                {
                    test: /\.(png|jpg|svg|ttf|eot|woff|woff2)$/,
                    use: [
                        {
                            loader: 'url-loader',
                            options: {
                                limit: 8192,
                                name: '[path][name].[ext]'
                            }
                        }
                    ]
                }
            ],

            noParse: [
                /jquery\.js$/
            ]
        },

        plugins: [
            new webpack.ProvidePlugin({
                $: "jquery",
                jQuery: "jquery",
                "window.jQuery": "jquery"
            }),

            new webpack.NoEmitOnErrorsPlugin(),

            new MiniCssExtractPlugin({
                filename: "css/[name].css",
                allChunks: true
            }),

            new Clean(__dirname + '/dist/app')
        ],

        devtool: PRODUCTION ? false : 'inline-source-map'
    };

    if (PRODUCTION) {
        config.plugins.push(
            new webpack.optimize.UglifyJsPlugin({
                compress: {
                    // don't show unreachable variables etc
                    warnings: false,
                    drop_console: true,
                    unsafe: true
                }
            })
        );
    }

    return config;
};