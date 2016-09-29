FROM ashander/rpy:r2.3.2-py3.4.4-stretch

MAINTAINER Jaime Ashander "jashander@ucdavis.edu"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		nodejs npm \
	&& rm -rf /var/lib/apt/lists/*

RUN npm install -g gulp && ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install gulp-imagemin imagemin-pngquant imagemin-jpegoptim

CMD ["bash"]
