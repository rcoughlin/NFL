import gulp from        'gulp';
import webpack from     'webpack';
import uglify from      'gulp-uglify';
import less from        'gulp-less';
import minify from      'gulp-minify-css';
import { argv } from    'yargs';

const ES6_DIR = './src/js/**/*.es6',
    LESS_DIR = './src/less/**.less';

gulp.task('webpack', doWebpack);
gulp.task('less', function() {
    return gulp.src('./src/less/index.less')
        .pipe(less())
        .pipe(gulp.dest('./static/css'));
});
gulp.task('default', [ 'webpack', 'less' ]);
gulp.task('watch:es6', [ 'webpack' ], function() {
    gulp.watch(ES6_DIR, [ 'webpack' ]);
});
gulp.task('watch:less', [ 'less' ], function() {
    gulp.watch(LESS_DIR, [ 'less' ]);
});
gulp.task('watch', [ 'webpack', 'less' ], function() {
    gulp.watch([ ES6_DIR, LESS_DIR ], [ 'webpack', 'less' ]);
});

function doWebpack(cb) {
    const JS_DIR = './static/js',
        FILENAME = 'play.js';

    webpack({
        entry: `./src/js/play.es6`,
        module: {
            loaders: [
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
        },
        resolve: {
            React: '../../bower_components/react/react'
        },
        output: {
            path: JS_DIR,
            filename: FILENAME
        }
    }, function(e) {
        if (e) {
            throw new Error(e);
        }

        cb();
        // gulp.src(`${JS_DIR}/${FILENAME}`)
        //     .pipe(uglify({ mangle: false }))
        //     .pipe(gulp.dest(JS_DIR).on('end', cb));
    });
}