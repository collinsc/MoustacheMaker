const path = require('path');

module.exports = {
    entry: path.resolve(__dirname, 'application/static/scripts/index.js'),
    mode : "development",
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'application/static/webpack_components'),
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                      loader: "babel-loader"
                }
            }
        ]
    }

};