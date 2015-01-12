Title: Negative results or technical problems?
Date: 2009-11-02
Tags: musing, science, inference, ethics
Slug: Omitting-negative-results
Author: Jaime Ashander


True or false: "Non-publication of negative results is extraordinarily common in science...." ?

This comes from biomed world, specifically protein design, where some
awesome claims---design of protein receptors to detect TNT (the
explosive) among other things---have [come under
scrutiny](http://www.nature.com/news/2009/091012/full/news.2009.998.html).
The lab involved [recently retracted some other
work](http://www.nature.com/news/2008/080509/full/453275a.html).

The quotation above is from Loren Looger, who was a PhD student on the
project. He's referrring to unreported instances where a designed
protein didn't bind the target and concludes that the omission "did
not seem inappropriate." This brings up an important distinction, I
think, between negative results and experimental or procedural
problems.

I'm not an experimentalist, but I'll draw an analogy with
*coding*. Let's say you're coding up a simulation for a random walk on
a one-dimensional lattice with the goal of estimating the waiting time
to reach a certain node, #N#. Let's say you don't realize there's an
exact calculation for this, but you do have some idea about the
distribution that the simulation should produce. You use that expected
distribution in debugging and error checking. Your first version
produces answers that don't fit your distributional expectations, you
find some errors and you fix them . The next version seems right. Then
you do 10,000 simulations of 2000 steps each to find the waiting time
to reach *N* (let's say N << 2000). You report the waiting time as the
average of the 10,000 runs, discarding the results of the first
version.

In this case it seems perfectly reasonable to not discuss the errors
in getting the code right in reporting the results. The erroneous code
and the results it produced represent technical issues encountered on
the way to real, reportable results.

Let's say however, you were interested in the probability that of ever
reaching *N*. You should similarly report that probability as the
proportion of the 10,000 runs that _ever_ reached *N*. If you
discarded the results that never reached *N* you would say the
probability is 1. In this case you would be omitting _real_ (but
negative) _results_ and mis-reporting your findings.

I wonder, to which type of "negative results" is Looger referring?
