const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const webpack = require('webpack');

module.exports = merge(common, {
    mode: 'development',

    output: {
        publicPath: 'http://localhost:3000/assets/dist/',
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
    ],

});
