---
title: R markdown post using rmd_reader
author: Jaime Ashander
status: draft
tags: help, tag me, i'm a tag
output:
     md_document:
         variant: markdown_strict
         dev: 'svg'
         encoding: 'UTF-8'
date: 2015-04-25
---

    params <- rnorm(100)
    plot(params, rnorm(100))

![My
alt1]({attach}example-rmd_files/figure-markdown_strict/my-fig-1.svg)

    cat("\n\n")

    hist(params)

![alt2]({attach}example-rmd_files/figure-markdown_strict/my-fig-2.svg)

[intrasite link]({filename}example-yaml.md)

    print(knitr::knit_hooks$get('plot'))

    ## function(x, options) {
    ##              if (!is.null(options$pelican) && options$pelican)
    ##                  x <- paste0("\\{attach\\}", x)
    ##              knitr::hook_plot_md(x, options)
    ## }
    ## <environment: 0xa257970>
