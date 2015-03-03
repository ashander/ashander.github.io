Title: Between-generation bet-hedging
Author: Jaime
Date: 2015-01-12
Tags: stochastic life histories, evolution, stochasticity

Version of notes for discussion I led in
[Sebastain Schreiber's](http://www.eve.ucdavis.edu/sschreiber/) for
PBG 271 Research Conference in Ecology on "Life history evolution in
stochastic environments".


### Reading Childs et al and Stearn's piece on Bernoulli

[Childs, Metcalf and Rees (2010)](doi:10.1098/rspb.2010.0707) present
a plant-focused review of bet-hedging, including a review of essential
theory.  As in many papers on bet-hedging, these authors distiguish
between conservative and diversified strategies.

#### Geometic mean fitness concept

>When fitness is temporally variable, the appropriate measure of
>evolutionary success is the expected geometric mean growth rate of a
>genotype. This is because fitness, like population growth, is an
>inherently multiplicative process that is very sensitive to
>occasional low values. -- Childs et al 2011

Let's remind ourselves why.

Following roughly the notation of Frank and Slatkin (1990), let $x_i$ the frequency of genotype $i$ and $R_i(t)$ the mean fitness of genotype $i$ in year $t$, then
genotype frequency $i$ changes as
$$
x_i(t+1) = \frac{R_i(t)x_i(t)}{R_1(t)x_1(t) + R_2(t)x_2(t)}
$$
Setting $y(t) = x_1(t)/x_2(t)$, we get
$$
y(t+1)=[R_1(t)/R_2(t)]y(t)
$$
Hence, $y(t) = y(0) \prod_{i=0}^{t-1} \lambda(i)$ where $\lambda(t) =
R_1(t)/R_2(t)$ is a (non-standard) relative fitness measure.

We can rearrange this and take logs to see $\tfrac{1}{t} \log
(y(t)/y(0)) = \tfrac{1}{t} \sum_{i=0}^{t-1} \log \lambda(i)$. Applying
the law of large numbers, $E[\log \lambda(t)]$ determines whether
genotype 1 "wins" (i.e. expectation is >0) or "loses"
(i.e. expectation is <0).But this ($(\prod_t
\lambda(i))^{\tfrac{1}{t}}$) is the geometric mean fitness!

<!-- If so, please remind folks about the approximation of $E[\log R_1(t)]$
when $R_1(t)=1+s_i(t)$ where $s_i(t)$ has mean zero and is "small". -->


#### So the stochastic growth rate _is_ the geometric mean fitness

And these are the appropriate measure of success for long-term evolution in a varying environment.
Stochastic growth rate $\rho$ (in Childs' notation) with $\lambda(i)$ fitness in generation $i$ is

$$
\rho = E [ \log (\lambda(i)) ]
$$

Which we just saw above is the geometic mean fitness.

#### So how does this lead to a mean-variance tradeoff?

<!-- The geometric mean fitness over $t$ generations
is $(\prod_n \lambda(t))^{\tfrac{1}{t}}$.  Taking the logarithm of
this, $\tfrac{1}{t} \sum_t \log(\lambda(i))$, which is $\rho$ above. -->

As Childs et al note, Jensen's inequality here implies the geometic
mean fitness is less than the arithmetic mean $\rho \le \log
E[\lambda(i)]$.


More specifically, as Sebastian mentioned last week, we can take a
Taylor approximation,

$$
E[f(x)] \approx f( E[x]) + \tfrac{1}{2}
f''(E[x]) {\rm Var}(x).
$$

With $f = \log$ this gives

$$
E[\log (\lambda)] \approx \log (E[\lambda]) - \tfrac{1}{2
E[\lambda]^2} {\rm Var}(\lambda),
$$

implying the magnitude of the decrease from arithmetic to geometic
mean fitness is proportional to the squared coefficient of variation
in fitness.  In fact, if $\lambda(i) \approx 1 + \epsilon_i$ with
$\epsilon$ a "small" random variable with mean zero this gives the
common approximation to the stochastic growth rate $\lambda_S \approx
\bar \lambda - \tfrac{1}{2} \sigma_\lambda^2$.


This leads to Slatkin's (1974) coining of _evolutionary bet-hedging_
to denote the resulting "tradeoff" where strategies with lower
arithmetic mean fitness can invade against those with higher
arithmetic mean fitness (if they have lower variance).

### Discussion points

* is "tradeoff" a good term here? doesn't evolution just favor the maximizer of geometric mean fitness?
* evidence for bet hedging in nature. what is needed and what has been shown?
* BH in structured populations -- IPMs are suggested as means for analyzing, what are obstacles to getting there (e.g. data limitation)?
* conservative versus diversified BH: how to connect this terminology to
  our framework? Any concise model of "conservative" BH?
* whose fitness is it?


<!--
```R
code
```

\begin{equation}
\exp{x}
\end{equation}
-->
