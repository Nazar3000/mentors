const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const path = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = merge(common, {
    mode: "production",
    output: {
        path: path.resolve('./assets/dist/'),
        publicPath: '/static/dist/'
    },
    plugins: [
        new UglifyJSPlugin({sourceMap: true}),
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production')
        })
    ]
});