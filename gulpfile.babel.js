import gulp from        'gulp';
import webpack from     'webpack';
import uglify from      'gulp-uglify';
import less from        'gulp-less';
import { argv } from    'yargs';

gulp.task('webpack', doWebpack);

gulp.task('less', function() {
    return gulp.src('./src/less/index.less')
        .pipe(less())
        .pipe(gulp.dest('./static/css'));
});

gulp.task('default', [ 'less' ], function() {
    let proms = [];

    for (let file of [ 'index.es6', 'mixpanel.es6' , 'play.es6' ]) {
        let prom = new Promise(function(resolve) {
            doWebpack(resolve, file);
        });

        proms.push(prom);
    }

    return Promise.all(proms);
});

gulp.task('watch:es6', function() {
    gulp.watch(`./src/js/${argv.filename}`, [ 'webpack' ]);
});
gulp.task('watch:less', function() {
    gulp.watch(`./src/less/${argv.filename}`, [ 'less' ]);
});

function doWebpack(cb, filename = '') {
    const FILENAME = (filename || argv.filename).replace('es6', 'js');

    webpack({
        entry: `./src/js/${filename || argv.filename}`,
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
        resolve: {},
        output: {
            path: './static/js',
            filename: FILENAME
        }
    }, function(e, stats) {
        if (e) {
            throw new Error(e);
        }

        gulp.src(`static/js/${FILENAME}`)
            .pipe(uglify({ mangle: false }))
            .pipe(gulp.dest('./static/js').on('end', cb));
    });
}