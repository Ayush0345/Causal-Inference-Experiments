# -*- coding: utf-8 -*-
"""iv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bRd2wmzeLSmwCV7Au4UeQrFRc4V-476S
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from itertools import combinations
from statsmodels.sandbox.regression.gmm import IV2SLS
import matplotlib.pyplot as plt

# (a) Setting random observation and seed for reproduction of results in each iteration
np.random.seed(42)

data = np.random.normal(size=10000)
data.shape # check shape for consistency of vector size

# (b) Generating random data for the instrumental variable in the form of a normal distribution with mean 2 and variance 1

Z = np.random.normal(loc = 2, scale = 1, size = 10000)
Z.shape # check shape for consistency of vector size

# (c) Generating random data for error terms in the form of a bivariate normal distribution with mean 0, variance 1, and correlation 0.8

mean = [0,0]
covariance = [[1,0.8],[0.8,1]]

error = np.random.multivariate_normal(mean, covariance, size = 10000)
error = pd.DataFrame(error, columns=['epsilon', 'x1'])
e = error['epsilon']
v = error['x1']

"""Normal Distribution with Mean = 0, Variance = 1 and Covariance = 0.8. Moreover, the covariance matrix must be positive semi-definite (eigenvalues are nonnegative) otherwise the behavior of this method will be undefined and backward compability will not be guaranteed. *(Papoulis, A., “Probability, Random Variables, and Stochastic Processes,” 3rd ed., New York: McGraw-Hill, 1991.)*"""

# (d) Data Generating Process for the Causal & First-Stage Model

delta = 0.5

X = Z + v
print(X)

Y = delta*X + e

# (e) OLS Estimates

X = sm.add_constant(X)
fs_model = sm.OLS(Y, X).fit()
print(fs_model.summary())

"""**OLS estimate δ = 0.9056**"""

# (f) 2SLS estimation using Z as an Instrument

exog = X
exog = sm.add_constant(exog)

instrument = Z
instrument = sm.add_constant(instrument)

IV_model = IV2SLS(endog = Y, exog = exog, instrument = instrument).fit()
print(IV_model.summary())

"""1st stage - **OLS estimate with OVB: δ = 0.9056**

2nd stage - **2SLS estimate: δ = 0.5025**

(g) The parameter value chosen randomly to generate the data was 0.5. In the first stage where we get delta with an omitted variable bias, we find that the estimate is 0.9056. In the second stage, the 2SLS estimator gave us a sufficiently close estimate of delta, i.e., 0.5025, to the parameter value we picked at the beginning of the experiment. Therefore, we can conclude that Z is a valid internal instrument to estimate the causal effect of X on Y.
"""
