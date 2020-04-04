#!/usr/bin/env python
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import scipy
from spipy.integrate import odeint

def derfunc(y,t):
    g = 32 # ft/s^2
    L = 2 # ft
    theta, omega = y
    dydt = [omega, -g/L * np.sin(theta)]
    return dydt
    
y0 = [0,10]
t = np.linspace(0,1,20)
sol = odeint(derfunc,y0,t)
plt.plot(t, sol[:,0],'b', label = 'theta(t)')
plt.plot(t, sol[:,1],'g', label = 'omega(t)')
plt.xlabel('t')
plt.show()