Title: This site
Template: etc


A long-overdue website redesign. My overall goal is to combine
personal academic website (papers, projects, CV, etc) along with a
platform for quick blog-like entries (perhaps later adding disqus
integration, share buttons etc).

Currently, pull data from figshare for results.
Eventually I'd like to automatically pull data from other sources (eg github). 


## Details

* templated (jinja2) index to pull from results (papers, preprints),
  themes (overall project categories) and notes (blog-like)
* will add projects (work in progress, github repos, project descriptions) as top-level category soon
* these categories are repeated on top nav
* rotating banner image with some shots from old website

# Engine + hosting

* Pelican engine for a static site to generate results, projects, notes from markdown
* hosting on github

# Style

* bootstrap, using bootswatch yeti via pelican-bootstrap3
* very light additional css (eg padding elements)
* customizations to pelican-bootstrap3 include rotating banner bar
  (via javascript in base template), limiting sidebar display to
  blog-like (called notes here) entries, and adding neighbor arrows to blog posts
