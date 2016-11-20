---
title: So, you did some GLMs & compared with AIC. Congrats!
author: Jaime Ashander
date: 2015-10-26
modified: 2015-12-14
tags: R, statistics, model selection, GLM, AIC, deviance
output:
    md_document:
        variant: markdown_strict
        dev: 'svg'
    encoding: 'UTF-8'
---

Here's what you need to report in a paper about the model comparison:

-   residual deviance
-   residual df
-   delta AIC
-   AIC weight

You should also report the null deviance and degrees of freedom, maybe
in a table caption.

Thanks to [Emilio Bruna](http://brunalab.org/) for prompting this post
and suggesting its title. (**Update 2015-12-14**: thanks also to Ben
Bolker for [pointing out some issues in the first version of this
post](https://github.com/ashander/ashander.github.io/commit/b25af179befbfdcdf013f7b484092296a0324bf6).)
Below I'll explain why you should include at least these numbers, do a
worked example, and mention some situations where it's better to use
something other than AIC.

### What to report

For model selection, a model's AIC is only meaningful relative to that
of other models, so Akaike and others recommend reporting differences in
AIC from the best model, *Δ**AIC*, and AIC *weight*. The latter can be
viewed as an estimate of the proportion of the time a model will give
the best predictions on new data (conditional on the models considered
and assuming the same process generates the data; this heuristic view
appears justified by simulations, e.g., Burnham and Anderson 2002 pp.
348). Also, neither differences in AIC less than 0.1 nor differences in
AIC weights below 0.01 are really meaningful, so round the reported
numbers appropriately.

Finally, even if using an information criterion include the residual
deviance and degrees of freedom for each model. These provide a (rough)
goodness of fit.

### Example: UC Berkeley admissions and gender

Let's look at the built-in `UCBAdmissions` data. As R will tell you,
these data are often used to illustrate Simpson's paradox (see
`?UCBAdmissions` and Bickel *et al.* 1975 or my PPS below).

    d <- as.data.frame(UCBAdmissions)
    d <- tidyr::spread(d, Admit, Freq) # use Hadley's excellent tidyr to reshape
    d[order(d$Dept), ]

    ##    Gender Dept Admitted Rejected
    ## 1    Male    A      512      313
    ## 7  Female    A       89       19
    ## 2    Male    B      353      207
    ## 8  Female    B       17        8
    ## 3    Male    C      120      205
    ## 9  Female    C      202      391
    ## 4    Male    D      138      279
    ## 10 Female    D      131      244
    ## 5    Male    E       53      138
    ## 11 Female    E       94      299
    ## 6    Male    F       22      351
    ## 12 Female    F       24      317

Using logistic regression, encode several models for the effect of
applicant gender, department identity, or both on admission.

    m1 <- glm(cbind(Admitted, Rejected) ~ Gender, d, family='binomial')
    m2 <- glm(cbind(Admitted, Rejected) ~ Dept, d, family = 'binomial')
    m3 <- glm(cbind(Admitted, Rejected) ~ Dept + Gender, d, family = 'binomial')
    model.names <- c("1 Gender", "2 Dept", "3 Gender + Dept")

(Note: although we might like to allow for an interaction between gender
and department, the data here are insufficient to fit such a model.)

Running `summary` on any one of the fits yields a bunch of stats: AIC,
Residual and null deviance, as well as coefficients, their standard
errors, and significance.

### How to do it in `R`

We could type by hand the AIC and other stats. No fun!

There are two other options.

First is to use [David Robinson](http://varianceexplained.org/)'s
`broom` which gives tidy summaries of model objects. The second is to
use [Ben Bolker](http://ms.mcmaster.ca/~bolker/)'s `bbmle` which
provides methods for generating pretty tables of xIC values.

#### Using broom

    summ.table <- do.call(rbind, lapply(list(m1, m2, m3), broom::glance))

If we take a look at `summ.table`, we'll see it has all the ingredients
we might like to report from model selection, whether via AIC, BIC, or
just the deviance. These are, in order, null.deviance, df.null, logLik,
AIC, BIC, deviance, df.residual.

Creating a table with our own desired columns in an appropriate order is
easy.

    table.cols <- c("df.residual", "deviance", "AIC")
    reported.table <- summ.table[table.cols]
    names(reported.table) <- c("Resid. Df", "Resid. Dev", "AIC")

    reported.table[['dAIC']] <-  with(reported.table, AIC - min(AIC))
    reported.table[['weight']] <- with(reported.table, exp(- 0.5 * dAIC) / sum(exp(- 0.5 * dAIC)))
    reported.table$AIC <- NULL
    reported.table$weight <- round(reported.table$weight, 2)
    reported.table$dAIC <- round(reported.table$dAIC, 1)
    row.names(reported.table) <- model.names

With my advice above in mind, here's *a minimal table for reporting
model selection on GLMs* using fitting results extracted with
`broom::glance`:

Caption: Model selection for the effect gender (model 1), department
(model 2), and both gender and department (model 3) on admission
probability fit to 12 observations (i.e., total degrees of freedom) with
877.056 null deviance.

    reported.table

    ##                 Resid. Df Resid. Dev  dAIC weight
    ## 1 Gender               10      783.6 753.9   0.00
    ## 2 Dept                  6       21.7   0.0   0.56
    ## 3 Gender + Dept         5       20.2   0.5   0.44

#### Using `bbmle`

    reported.table2 <- bbmle::AICtab(m1, m2, m3, weights = TRUE, sort = FALSE, mnames = model.names)
    reported.table2[["Resid. Dev"]]  <- summ.table[["deviance"]] # get the deviance from broom'd table

Caption: Model selection for the effect gender (model 1), department
(model 2), and both gender and department (model 3) on admission
probability fit to 12 observations (i.e., total degrees of freedom) with
877.056 null deviance.

    reported.table2

    ##                 dAIC  df weight Resid. Dev
    ## 1 Gender        753.9 2  <0.001 783.6     
    ## 2 Dept            0.0 6  0.56    21.7     
    ## 3 Gender + Dept   0.5 7  0.44    20.2

Of course, model selection is just the beginning of reporting your
results. See the PPS below for some thoughts on reporting results of the
best model(s).

And, before you even did model selection, you should have asked
yourself...

### Is AIC the right criterion?

-   For small data and frequentist inference, you should use AICc -- the
    small sample correction which provides greater penalty for each
    parameter but approaches AIC as *n* becomes large. If it makes a
    difference, you should use it. (I probably should have used
    it above.)
-   For large data and frequentist inference , consider BIC, which is
    asymptotically consistent while AIC is not (see Hastie *et al.*
    2009, which is available online). AIC typically favors
    overly-complex models with large *n* relative to BIC. Note, however,
    that this is not an issue for prediction, only inference of a *true*
    model (if one exists; Sec. 6.4 McElreath 2015).
-   For Bayesian models, consider [WAIC or
    LOO](http://andrewgelman.com/2015/07/16/new-papers-on-loowaic-and-stan/)
    (instead of DIC, which has issues with non-Gaussian posteriors
    McElreath 2015).
-   Don't use information criteria for model selection between GLMs with
    different link functions

### Further Reading & References

-   [Ben Bolker on reporting results in the text for
    GLMMs](http://ms.mcmaster.ca/~bolker/misc/GLMM_results_report.pdf)
    this is a piece of a larger chapter [GLMMs: worked
    examples](http://ms.mcmaster.ca/~bolker/R/misc/foxchapter/bolker_chap.html)
    that approaches inference as model checking and improvement (as
    opposed to multi-model inference *sensu* Burnham and Anderson 2004)
-   [Burnham, and Anderson.
    2004.](https://dx.doi.org/10.1177/0049124104268644) Multimodel
    Inference: Understanding AIC and BIC in Model Selection.
    *Sociological Methods & Research* 33(2):261-304
-   Burnham, and Anderson. 2002. *Model Selection and Multimodel
    Inference: A Practical Information-Theoretic Approach.*
    Second Edition. Springer.
-   [Elliot and Brook 2007](https://dx.doi.org/10.1641/B570708) for a
    short piece on the philosophical background of multiple working
    hypotheses
-   [Hastie, Tibshirani, and Friedman.
    2009.](http://statweb.stanford.edu/~tibs/ElemStatLearn/) Elements of
    Statistical Learning, Second Edition. Springer, New York, NY, USA.
-   [McElreath. 2015.](https://www.crcpress.com/Statistical-Rethinking-A-Bayesian-Course-with-Examples-in-R-and-Stan/McElreath/9781482253443)
    Statistical Rethinking. CRC Press.
-   [Brian O'Meara's AIC
    tutorial](http://brianomeara.info/tutorials/aic/)

### PS: Nested models

Reporting the residual deviance and degrees of freedom as above is
relatively similar to R's output for conducting an ANOVA on a GLM (where
you can optionally add a statistical test). For nested models, you may
as well just do this and report the table:

    m3.anova <- anova(m3, test="Chisq")
    round(m3.anova, digits = 4)

    ## Analysis of Deviance Table
    ## 
    ## Model: binomial, link: logit
    ## 
    ## Response: cbind(Admitted, Rejected)
    ## 
    ## Terms added sequentially (first to last)
    ## 
    ## 
    ##        Df Deviance Resid. Df Resid. Dev Pr(>Chi)    
    ## NULL                      11        877             
    ## Dept    5      855         6         22   <2e-16 ***
    ## Gender  1        2         5         20     0.22    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

### PPS: Evaluating the best model(s)

For the best model(s), you should then go on to visualize the fit
relative to the data (and report model results in the text).

To visualize the admissions data and mean fits from models 2 and 3
(which have approximately equal AIC weight), we can use `ggplot2` and
`augment` from broom (which adds model predictions and statistics to the
data).

To provide model-averaged predictions is a bit more work:

    m3.pred <- broom::augment(m3)
    m2.pred <- broom::augment(m2)
    m2.weight <- reported.table[2, "weight"]
    m3.weight <- reported.table[3, "weight"]
    mavg.pred <- m2.weight * m2.pred[ , -(1:2)] + m3.weight * m3.pred[ , -(1:3)]
    mavg.pred <- cbind(m3.pred[1:3], mavg.pred)

    library(ggplot2)
    ggplot(d) +
        geom_point(aes(Dept, Admitted / (Admitted + Rejected), color=Gender,
               size=Admitted + Rejected),
               position = position_dodge(width = 0.5)) +
        geom_pointrange(aes(Dept, plogis(.fitted),
                ymin = plogis(.fitted - 2 * .se.fit),
                ymax = plogis(.fitted + 2 * .se.fit),
                shape=Gender),
                position=position_dodge(width = 0.5), data =mavg.pred, alpha=0.4) +
        theme_minimal() + scale_color_manual(values=c("blue", "orange"))

![Admissions (open circles, size indicates total applicants) versus
deparatment and predictions from model 2 (department only, diamonds) and
model 3 (department and gender, dots and
triangles)](%7Battach%7Dmodel-selection-GLMs-AIC-what-to-report_files/figure-markdown_strict/model-viz-1.svg)

Admissions (colored dots, size indicates total applicants) versus
department from UCB Admissions data (included in `R`), and averaged
predictions (means ± 2 SE) from model 2 (department only) and model 3
(department and gender), with averaging by AIC weight.

#### Simpson's paradox

Comparing model 3 with model 1 illustrates Simpson's paradox. Without
accounting for department, the apparent effect of female gender on
admission is negative (female odds relative to male 0.543, *p* ≈ 0),
whereas after accounting for department, the (within-department) effect
is positive (but weak: female odds relative to male 1.105, *p*≈ 0.22).
