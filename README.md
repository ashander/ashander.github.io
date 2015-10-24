Github hosting for [my web site](http://ashander.github.com)

Originally built during my masters and hosted at `http://www.math.ualberta.ca/~ashander/`.

# Deploy

```sh

virtualenv site
pip install pelican Markdown PyYAML RPy2
mkdir plugins
git clone  https://github.com/getpelican/pelican-plugins.git plugins/pelican-plugins
# install my rmarkdown plugin
```

