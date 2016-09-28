FROM ashander/rpy

MAINTAINER Jaime Ashander "jashander@ucdavis.edu"

RUN echo "deb http://http.debian.net/debian sid main" > /etc/apt/sources.list.d/debian-unstable.list \
	&& echo 'APT::Default-Release "stretch";' > /etc/apt/apt.conf.d/default

#&& rm /etc/apt/sources.list.d/debian-unstable.list /etc/apt/apt.conf.d/default


RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		pandoc \
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

CMD ["bash"]
