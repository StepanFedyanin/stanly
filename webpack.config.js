'use strict';
/* webpack.config.js */

const path = require('path');

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const SpritePlugin = require('extract-svg-sprite-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

const devMode = process.env.NODE_ENV !== 'production';
const DIST = 'dist/';

module.exports = {
    devtool: false, //devtool: 'eval', // Enable to debug js code
    entry: {
            dist: [
                './src/css/style.scss',
                './src/js/index.js',
            ],

            // 'webgl-worker': './src/earth/worker.js'
            // 'earth': './src/earth/earth.js'

            // dist: './src/css/main.scss',
            // main: './src/js/index.js'
        },
    output: {
        path: path.resolve(__dirname, DIST),
        filename: devMode ? '[name].js' : '[name].[chunkhash].js',
    },
    plugins: [
        new CleanWebpackPlugin([DIST]), // clean folder 'dist'
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: devMode ? '[name].css' : '[name].[contenthash].css',
            chunkFilename: devMode ? '[id].css' : '[id].[contenthash].css',
        }),
        new LiveReloadPlugin({}),
        new SpritePlugin({
            filename: '[contenthash].svg'
        })
    ],
    module: {
        rules: [
            {
                enforce: "pre",
                test: /\.js$/,
                exclude: /node_modules/,
                loader: "eslint-loader", // enable eslint
                options: {
                    fix: true
                }
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
              test: /\.svg$/,
              use: [
                SpritePlugin.loader,
                'svg-transform-loader',
              ]
            },
            {
                test: /\.s?[ac]ss$/,
                use: [
                    'style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    SpritePlugin.cssLoader,
                    {
                        loader: 'sass-loader',
                        options: {
                            // data: '@import "vars.scss";', // I tried variables
                            // outputPath: 'css/',
                            includePaths: [path.resolve(__dirname, "src/css")],
                            outputStyle: 'compressed',
                            sourceMap: true,
                            outFile: 'style.css'
                        }
                    }
                ]
            },
            {
                test: /\.(gif|png|jpe?g|)$/i,
                use: [
                    'file-loader',
                    {
                      loader: 'image-webpack-loader',
                      options: {
                        name: '[name].[ext]',
                        outputPath: 'images/',
                        mozjpeg: {
                          progressive: true,
                          quality: 65
                        },
                        // optipng.enabled: false will disable optipng
                        optipng: {
                          enabled: false,
                        },
                        pngquant: {
                          quality: '65-90',
                          speed: 4
                        },
                        gifsicle: {
                          interlaced: false,
                        },
                        // the webp option will enable WEBP
                        webp: {
                          quality: 75
                        }
                      }
                    },
                ],
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                use: [
                  {
                    loader: 'file-loader',
                    options: {
                      name: '[name].[ext]',
                      outputPath: 'fonts/'
                    }
                  }
                ],
            },
        ]
    }
};