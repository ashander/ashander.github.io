var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant'); // $ npm i -D imagemin-pngquant
var imageminJpegoptim = require('imagemin-jpegoptim');
var exec = require('child_process').exec;
var path = require('path');
var tap = require('gulp-tap');
var log = require('gulp-util').log;


gulp.task('r-to-markdown', function (cb) {
  var gulp_dir = process.cwd();
  var content_dir = 'content/notes/';
  var working_dir = gulp_dir + '/' + content_dir;
  var command = 'Rscript format_pelican.R ' + '"' + working_dir + '"';
  return gulp.src(content_dir + '*.Rmd')
    .pipe(tap(function(file, t) {
      var rel_path = path.relative(working_dir, file.path);
      exec(command + ' "' + rel_path + '"',
          function(err, stdout, stderr) {
            log('Rendered: ' + stdout);
            if (stderr) {
              log('Error: ' + stderr);
            }
            if (err) {
              cb(err);
            }
          });
    }));
});


gulp.task('optimize-images', function () {
  return gulp.src('content/images/**/*')  // NB these globs break autoindent
  .pipe(imagemin({
    progressive: true,
    svgoPlugins: [
      {removeViewBox: false},
      {cleanupIDs: false}
    ],
    use: [pngquant(),
      imageminJpegoptim({max: 61})
    ]
  }))
  .pipe(gulp.dest('output/images'));
});
