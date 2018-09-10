const path = require("path");
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const WebpackMd5Hash = require('webpack-md5-hash');


module.exports = {
    context: __dirname,

    entry: {
        index: '../apps/static/scripts/index',
    },

    output: {
        path: path.resolve('../assets/dist/'),
        publicPath: '../assets/dist/',
        filename: "[name]-[hash].js",
    },

    plugins: [
        new BundleTracker({filename: './webpack/webpack-stats.json'}),
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({
          filename: 'style.[contenthash].css',
        }),
        new WebpackMd5Hash()
    ],

    module: {
        rules: [
            {
                test: /\.js?$/, exclude: /node_modules/, use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['stage-2']
                    }
                }
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    hotReload: true
                }
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.scss$/,
                use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader']
              },
            {
                test: /\.(ttf|eot|svg|gif|jpg|jpeg|png)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {}
                    }
                ]
            }
        ],
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        modules: ['node_modules'],
        extensions: ['.js']
    }
};
