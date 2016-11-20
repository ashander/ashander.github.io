Github hosting for [my web site](http://ashander.github.com)

Originally built during my masters and hosted at `http://www.math.ualberta.ca/~ashander/`.

# Deploy

```sh
conda create -n site
source activate site
pip install pelican Markdown PyYAML RPy2 ghp-import
mkdir plugins
git clone  https://github.com/getpelican/pelican-plugins.git plugins/pelican-plugins
make publish
make devserver # examine localhost:8000
```

