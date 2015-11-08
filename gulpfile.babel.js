

import webpack from  'webpack'


gulp.task('webpack', function(cb) {
    webpack({
        entry: './src/play.es6',
        module: [
            {
                test: /\.json$/,
                loader: 'json-loader'
            },
            {
                test: /\.coffee$/,
                loader: 'coffee-loader'
            },
            {
                test: /\.es6$/,
                loader: 'babel-loader'
            },
            {
                test: /\.s?css$/,
                loader: 'style!css!sass'
            }
        ],
        resolve: {},
        output: {
            path: './static/js',
            filename: 'play.js'
        }
    }, function(e) {
        if (e) {
            throw new Error(e);
        }

        gulp.src('./static/play.js')
            .pipe(uglify({ mangle: false }))
            .pipe(gulp.dest('./static/play.js').on('end', cb));
    });
});