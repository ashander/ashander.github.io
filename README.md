Github hosting for [my web site](http://ashander.github.com)

Originally built during my masters and hosted at `http://www.math.ualberta.ca/~ashander/`.

# Deploy

```sh
git clone --recursive --j8 <this repo>
cd <this repo>
conda create -n site
source activate site
pip install pelican Markdown ghp-import
npm install .
make publish
make devserver # examine localhost:8000
```

