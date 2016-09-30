FROM ashander/rpy:r2.3.2-py3.4.4-stretch

MAINTAINER Jaime Ashander "jashander@ucdavis.edu"

RUN echo "deb http://http.debian.net/debian sid main" > /etc/apt/sources.list.d/debian-unstable.list \
	&& echo 'APT::Default-Release "stretch";' > /etc/apt/apt.conf.d/default

#&& rm /etc/apt/sources.list.d/debian-unstable.list /etc/apt/apt.conf.d/default


RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		pandoc nodejs npm\
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir\
        pelican \
	Markdown \
	PyYAML \
	RPy2 \
	ghp-import \
	&& install2.r --error \
	rmarkdown \
	lintr \
	lme4 \
	tidyr\
	car \
	broom \
	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds


RUN npm install -g gulp && ln -s /usr/bin/nodejs /usr/bin/node && \
    npm install gulp-imagemin imagemin-pngquant imagemin-jpegoptim

RUN install2.r --error \
	bbmle\
	lsmeans\
	gridExtra\
	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds

CMD ["bash"]
