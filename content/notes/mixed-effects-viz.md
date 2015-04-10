Title: Mixed effects viz for d-rug
Slug: D-RUG-mixed-effects-viz
Date: 2015-04-10
Author: Jaime Ashander

Post is a stub with R code to walk through.

```R

## ----knit-opts, echo=FALSE-----------------------------------------------

knitr::opts_chunk$set(cache=TRUE)



## ----help----------------------------------------------------------------
help(package='lme4')
??lme4
methods(class='merMod')


## ----load----------------------------------------------------------------
d <- read.delim("http://datadryad.org/bitstream/handle/10255/dryad.41984/Maestre_Ecol88.txt?sequence=1")
recode <- car::recode

d <- within(d, {
            nutrient_hetero <- recode(factor(nh), "1='homogeneous'; 2='heterogeneous'")
            nutrient_add <- recode(factor(na), "1='40 mg N'; 2='80 mg N'; 3='120 mg N'")
            water_hetero <- recode(factor(wh), "1='homogeneous'; 2='pulse'")
            water_add <- recode(factor(wa), "1='125 mL'; 2='250 mL';3='375 mL'")
        })


## ----lme-models, warning=FALSE-------------------------------------------

## riiindex --root depth allocation
library(lme4)

m1 <- lmer(riiratio ~ nutrient_add * nutrient_hetero  *  water_add   +
           water_hetero +  (1 | block), data=d)

## we'd might like to use model that includes varying sopes
## watering seems the most likely to have block-level differences ?
m2 <- lmer(riiratio  ~ nutrient_add * nutrient_hetero  *  water_add +  water_hetero +
               (water_hetero | block), data=d)
## first diagnostic -- very high correlation is bad
VarCorr(m2)

plot(m1, type=c("p", "smooth") ) ## concerning increase in variance with fitted
plot(m1, resid(.) ~ fitted(.) | block, abline=c(h=0), lty=1,  type=c("p", "smooth")) # per block
plot(m1, sqrt(abs(resid(.))) ~ fitted(.) | block,  type=c("p", "smooth"))


# residuals look better for more complex RE structure
lattice::qqmath(m1, id=0.05, group=block)

## look at randeom effect
lattice::dotplot(ranef(m1, condVar=TRUE)) #were we to have LOTS of RE, using lattice::qqmath for y axis spacing based on quantiles of standard normal -- is better to distinguish important few from "trivial many"

system.time(m1.prall <- profile(m1))
system.time(m1.prre <- profile(m1, which='theta_'))

#  plots
# the 'profile zeta plot'
# linear indicatesa a quadratic likelihood profile, and so Wald approximations for CI will work well
# random effects parameters on a standard deviation (or correlation) scale
lattice::xyplot(m1.prre)
lattice::xyplot(m1.prall)

# the 'profile density plot'
# approximate probability density functinos of the parameters
# -- distros underlying profile confidence intervals
# linear zeta plot <==> gaussian densities
lattice::densityplot(m1.prall)

# the 'profile pairs plot'
# bivariate confidence regions baed on profile
# 'profile traces' -- cross hairs -- are conditinoal estimates  of one parmeter given the other
# above-diag: estimated scale
# below-diag: 'zeta' scale, some sense, the best possible set of single-parameter transformations for assessing the contours"
lattice::splom(m1.prre)




## ----ryo-----------------------------------------------------------------

make_CI_df <- function(modprof, model, BOOT=FALSE, ...) {
  ci <- confint(model, method='Wald')
  cip <- confint(modprof)
  if(BOOT) {
      cib <- confint(model, method="boot", ...)
      cib_dat <- data.frame(cib, parameter=row.names(cib), type='Boot')
      names(cib_dat)[1:2] <- colnames(cib)
  }
  ci_dat <- data.frame(ci, parameter=row.names(ci), type='Wald')
  names(ci_dat)[1:2] <- colnames(ci)
  cip_dat <- data.frame(cip, parameter=row.names(cip), type='Prof')
  names(cip_dat)[1:2] <- colnames(cip)
  if (!BOOT) {
      ci_all_dat <- rbind(ci_dat, cip_dat)
  } else {
      ci_all_dat <- rbind(ci_dat, cip_dat, cib_dat)
  }
  fe_dat <- data.frame(parameter=names(fixef(model)), value=fixef(model))
  list(mean=fe_dat, bounds=ci_all_dat)
}

if(require(ggplot2)) {

    m1_ci <- make_CI_df(m1.prall, m1, BOOT=TRUE, nsim=100)
    m1_mean <- m1_ci[['mean']]
    m1_bnd <- m1_ci[['bounds']]

  ggplot(m1_bnd[m1_bnd$parameter != '(Intercept)', ]) +
          geom_linerange(aes(parameter, ymax=`97.5 %`, ymin=`2.5 %`, color=type),
                         position=position_dodge(w=.5), size=1.5) +
                           geom_hline(yintercept=0, linetype=2) +
                               coord_flip() + theme_minimal() +
                                   geom_point(aes(parameter, value),
                                              size=3, shape=3,
                                              data=m1_mean[m1_mean$parameter != '(Intercept)', ])
  
                                                    }

##   strong effect ot nutreint homogenetity
##   effect of adding lots of water
   ## nutreint has some effect

   ## look at consequences
if(require(lsmeans)){

    lsmip(m1, ~ nutrient_add  | nutrient_hetero * water_add)

    m1.lsm <- lsmeans(m1, ~ nutrient_add  | nutrient_hetero  * water_add)
    plot(m1.lsm, layout =c(2, 3), horizontal=FALSE)

    m1.lsm <- lsmeans(m1, ~ water_add | nutrient_add )
    plot(m1.lsm, horizontal=FALSE)

    m1.lsm <- lsmeans(m1, ~ nutrient_hetero * water_add | nutrient_add )
    plot(m1.lsm)


}



## ----latimer-fits--------------------------------------------------------

d2 <- read.delim("http://datadryad.org/bitstream/handle/10255/dryad.33579/Richmond%20et%20al%202011%20Datafile.txt?sequence=1")
names(d2) <- gsub('\\.', '', names(d2))

# rescale geo dist, sizediff
d2 <- within(d2, {
    geodist_scl <- (GeoDist - mean(GeoDist)) / var(GeoDist)
    sizediff_scl2 <- ((SizeDiff - mean(SizeDiff)) / var(SizeDiff))^2
    Series <- factor(Series)
    Female <- factor(Female)
    Male <- factor(Male)
    })

system.time(
    gm0 <- glmer(cop ~   sizediff_scl2   + (1 | Series) + (1 | Male)  + (1 | Female) ,
                 data=d2, family='binomial'))

gm1 <- glmer(cop ~ geodist_scl +  sizediff_scl2 + (1 | Series) + (1 | Male)  + (1 | Female) ,
             data=d2, family='binomial')


## ----latimer-crit--------------------------------------------------------

anova(gm1, gm0)

plot(gm0, type=c("p") ) #non useful
plot(gm0, factor(Series)  ~ resid(.),  abline=c(v=0), lty=2) # better than default eh
plot(gm0, sqrt(abs(resid(.))) ~ fitted(.) | Series )

if(require(gridExtra)) {
    do.call(gridExtra::grid.arrange, c(lattice::qqmath(ranef(gm0, condVar=TRUE)), list(nrow=1)))
} else {
    lattice::qqmath(ranef(gm0, condVar=TRUE))
    }
## useful if you have a lot of RE to draw attention to strong ones
## maybe latter == dot = sample size?

## no reason to retain RE on Male, but also drop Female
## no real justification, very slow profiling for many RE
#gm0noindre <- glmer(cop ~   sizediff_scl2   + (1 | Series), data=d2, family='binomial')

system.time(
    gm0.prall <- profile(gm0noindre, devtol=1e-6) # see https://stat.ethz.ch/pipermail/r-sig-mixed-models/2014q3/022394.html
)


## ----latimer-prof, eval=FALSE--------------------------------------------
## 
## #system.time(
## #    gm0_full.prall <- profile(gm0, devtol=1e-6)
## #)
## #   user  system elapsed
## #344.092   0.539 344.613


## ----latimer-plotting, warning=FALSE-------------------------------------

lattice::xyplot(logProf(gm0.prall))
lattice::densityplot(gm0.prall)
lattice::splom(gm0.prall)

## add ci plots

if(require(ggplot2)) {
  gm0_ci <- make_CI_df(gm0.prall, gm0)
  gm0_mean <- gm0_ci[['mean']]
  gm0_bnd <- gm0_ci[['bounds']]
  g <- ggplot(gm0_bnd[gm0_bnd$parameter != '(Intercept)', ]) +
          geom_linerange(aes(parameter, ymax=`97.5 %`, ymin=`2.5 %`, color=type),
                         position=position_dodge(w=.5), size=1.5) +
                           geom_hline(yintercept=0, linetype=2) +
                               coord_flip() + theme_minimal() +
                                   geom_point(aes(parameter, value),
                                              size=3, shape=3,
                                              data=gm0_mean[gm0_mean$parameter != '(Intercept)', ])

  g

  }


## ----low-magnitude-param, warning=FALSE----------------------------------
  g + scale_y_log10()




## ----prediction-visual---------------------------------------------------
## predicted effect
d2$pred_overall_gen <- predict(gm0, type='response', re.form=NA)
d2$pred_overall <- predict(gm0, type='response')
d2$pred_ind <- predict(gm0, type='response', re.form=~ (1|Female))
d2$pred_trial <- predict(gm0, type='response', re.form=~(1|Series))

d2_plus_count <- merge(d2, as.data.frame(table(Series=d2$Series)))

if(require(ggplot2)) {
g <-  ggplot(d2_plus_count) + geom_point(aes(SizeDiff, cop),
                                         position=position_jitter(h=0.05, w=0)) +
    geom_line(aes(SizeDiff, pred_trial, color=Series)) +
    geom_point(aes(SizeDiff, pred_ind, alpha=as.numeric(Female))) +
    geom_line(aes(SizeDiff, pred_overall_gen), color='red', size=1.5) +
    theme_minimal()
g


}




## todo - figure out ls means quick vis for variety of predictor values




## ----ugly-plot-----------------------------------------------------------

g + geom_line(aes(SizeDiff, pred_overall), color='darkgray', size=1) 



## ----post-pred-----------------------------------------------------------

## without RE
set.seed(1141)
gm0.sim_wo <- simulate(gm0, nsim=1000, re.form=NA)
sims <- sapply(gm0.sim_wo, function(x)  x)
ones <- colSums(sims)
zeros <- -colSums(sims-1)
perc <- ones/nrow(d2)
cvar <- apply(sims, 2, var)

## with RE
gm0.sim <- simulate(gm0, 1000 )
sims <- sapply(gm0.sim, function(x)  x)
re_ones <- colSums(sims)
re_zeros <- -colSums(sims-1)
re_perc <- re_ones/nrow(d2)
re_cvar <- apply(sims, 2, var)

pp_comp <- function(dist, cmp_fn, data, ...) {
  hist(dist, col='orange', xlab='value', ...)
  abline(v=cmp_fn(data), lwd=4, col='blue', lty=2)
}

op <- par(mfrow=c(2,4))
  pp_comp(ones, function(x) sum(x$cop), d2, main='ones - no RE', xlim=c(45, 110))
  pp_comp(zeros, function(x) -sum(x$cop - 1), d2, main='zeros -no RE', xlim=c(120, 185))
  pp_comp(perc, function(x) sum(x$cop)/nrow(d2), d2, main='% cop - no RE', xlim=c(0, .8))
  pp_comp(cvar, function(x) var(x$cop), d2, main='var - no RE', xlim=c(0.1, .3))

  pp_comp(re_ones, function(x) sum(x$cop), d2, main='ones - all RE', xlim=c(45, 110))
  pp_comp(re_zeros, function(x) -sum(x$cop - 1), d2, main='zeros - all RE', xlim=c(120, 185))
  pp_comp(re_perc, function(x) sum(x$cop)/nrow(d2), d2, main='% cop - RE', xlim=c(0, .8))
  pp_comp(re_cvar, function(x) var(x$cop), d2, main='var - all RE', xlim=c(0.1, .3))
par(op)



## ----glmmadmb-too, eval=FALSE--------------------------------------------
## ## look at glmmadmb too -- not evaluated
## gm1admb <- glmmadmb(cop ~ geodist_scl +  sizediff_scl2, random= ~1 | Series + 1 | Female , data=d2, family='binomial')
## 
## d2 <- data.frame(d2, predict(gm1admb, interval='confidence', type='link'))
## 
## plot(cop ~ SizeDiff, d2, ylim = c(0, 1))
## lines(plogis(fit) ~ SizeDiff, d2, lwd=2)
## lines(plogis(lwr) ~ SizeDiff, d2, lty=2, lwd=2)
## lines(plogis(upr) ~ SizeDiff, d2, lty=2, lwd=2)
##       geom_line(aes(SizeDiff, plogis(lwr)), color='red', size=1, linetype=2) +
##     geom_line(aes(SizeDiff, plogis(upr)), color='red', size=1, linetype=2) +


## ----broom-fortify-------------------------------------------------------


if(require(ggplot2)) {
    d_fort <- ggplot2::fortify(m1, d)
    str(d_fort)
}

if(require(broom)) {
    glance(m1)
    str(tidy(m1))
    str(augment(m1, d))
}


```
