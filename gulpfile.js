var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant'); // $ npm i -D imagemin-pngquant
var imageminJpegoptim = require('imagemin-jpegoptim');

gulp.task('default', function() {
  return gulp.src('content/images/**/*')
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
