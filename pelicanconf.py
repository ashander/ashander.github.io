#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jaime Ashander'
SITENAME = 'Jaime Ashander'
SITEURL = 'www.ashander.info'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/ashander'),
          ('Twitter', 'https://twitter.com/jaimedash'),
          ('figshare', 'http://figshare.com/authors/Jaime_Ashander/505494'),)


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# static paths copied without parsing
STATIC_PATHS = ['images', 'extra/custom.css', 'extra/CNAME',
                'extra/README' , 'extra/LICENSE' ]
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/README': {'path': 'README.md'},
    'extra/LICENSE': {'path': 'LICENSE.md'}
}

## menu setup
HIDE_SITENAME = True
DISPLAY_PAGES_ON_MENU = True

# images
BANNER = "images/header/bamfield.jpg"
BANNER_ALL_PAGES = True
BANNER_SUBTITLE = "rapid evolution: theory, computation, inference"

# Categories, tags, etc
USE_FOLDER_AS_CATEGORY = True
SLUGIFY_SOURCE = 'basename' # use filename as slug source

DEFAULT_DATE_FORMAT = ('%a %d %B %Y')

AUTHOR_SAVE_AS = ''
AUTHOR_URL = ''

ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"

CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
REVERSE_CATEGORY_ORDER = True

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

## Generate yearly archive
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

## Show most recent posts first
NEWEST_FIRST_ARCHIVES = True

# Style
THEME = "themes/pelican-bootstrap3"
BOOTSTRAP_THEME = 'yeti'
BOOTSTRAP_NAVBAR_INVERSE= True

CUSTOM_CSS = 'static/custom.css' # for spacers

## custom templated page for index
TEMPLATE_PAGES = { 'index.html': 'index.html'}
#, 'projects/index.html': 'projects/index.html'}

# fix for attempt to read index.html from http://www.voidynullness.net/blog/2014/11/30/upgrading-pelican-3-5/
READERS = {'html': None}
## direct

EXTRA_TEMPLATES_PATHS = ['templates/']
PAGE_PATHS = ['pages', 'etc']

# Plugins
PLUGIN_PATHS = [ "/Users/jaime/sites/pelican-plugins", ]
PLUGINS =  ['latex', 'neighbors', 'summary', 'related_posts', 'render_math', 'optimize_images']
# https://github.com/getpelican/pelican-plugins/tree/master/render_math
