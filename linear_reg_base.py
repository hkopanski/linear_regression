# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:10:43 2020

@author: hkopansk
"""

from scipy.stats import t
import matplotlib.pyplot as plt

data = {'beers': [5,2,9,8,3,7,3,5,3,5,4,6,5,7,1,4],
        'BAC': [0.1,0.03,0.19,0.12,0.04,0.095,0.07,0.06,0.02,0.05,0.07,0.1,0.085,0.09,0.01,0.05]}

dk  = []
dv1 = []

for k,v in data.items():
    dk.append(k)
    dv1.append(v)

def average_value(x):
    n = len(x)
    total = sum(x)
    return total/n

mu0 = average_value(dv1[0])
mu1 = average_value(dv1[1])

Sxx_t = []
Syy_t = []
Sxy_t = []
SSE_t = []

for i in range(len(dv1[0])):
    element_xx = (dv1[0][i] - mu0)**2
    element_yy = (dv1[1][i] - mu1)**2
    element_xy = (dv1[0][i] - mu0)*(dv1[1][i] - mu1)
    Sxx_t.append(element_xx)
    Syy_t.append(element_yy)
    Sxy_t.append(element_xy)
    
Sxx = sum(Sxx_t)
Syy = sum(Syy_t)
Sxy = sum(Sxy_t)

r = Sxy / (Sxx*Syy)**0.5
r_sqr = r**2
slope =  Sxy / Sxx
intercept = mu1 - mu0*slope

for i in range(len(dv1[0])):
    SSE_t.append((dv1[1][i] - slope*dv1[0][i] - intercept)**2)
    
SSE = sum(SSE_t)
s = (SSE/(len(dv1[0])-2))**0.5
seB1 = s / Sxx**0.5

CI      = []
CI_low  = []
CI_high = []
PI      = []
PI_low  = []
PI_high = []
  
x_vals = list(range(min(dv1[0])-1,max(dv1[0])+1))

def linreg(x):
    y = slope * x + intercept
    return y

y_vals = list(map(linreg,x_vals))

for i in range(len(x_vals)):
    CI.append(t.ppf(0.975, len(x_vals)-2)*s*(1/len(x_vals)+(x_vals[i] - mu0)**2/Sxx)**0.5)
    CI_low.append(y_vals[i] - CI[i])
    CI_high.append(y_vals[i] + CI[i])
    PI.append(t.ppf(0.975, len(x_vals)-2)*s*(1 + 1/len(x_vals)+(x_vals[i] - mu0)**2/Sxx)**0.5) 
    PI_low.append(y_vals[i] - PI[i])
    PI_high.append(y_vals[i] + PI[i])
 
print("The slope is: {} \nThe intercept is: {} \nThe R square value is: {}".format(slope, intercept, r_sqr))
      
fig, ax = plt.subplots(figsize = (8,5), dpi = 300)

ax.plot(x_vals,y_vals, c = '#253494', label = 'Regression Line')
ax.plot(x_vals,CI_low, c = '#2c7fb8', linestyle = '-.', label = 'Confidence Limit')
ax.plot(x_vals,CI_high, c = '#2c7fb8', linestyle = '-.')
ax.plot(x_vals,PI_low, c = '#41b6c4', linestyle = '--', label = 'Prediction Limit')
ax.plot(x_vals,PI_high, c = '#41b6c4', linestyle = '--')  
ax.fill_between(x_vals,CI_low, CI_high, alpha = 0.35, color = '#ffffcc')
ax.scatter(dv1[0],dv1[1], marker = '.', c = '#000000')
ax.scatter(mu0, mu1, marker = 'x', c = 'red')     

plt.grid()
plt.legend()
plt.show()
    