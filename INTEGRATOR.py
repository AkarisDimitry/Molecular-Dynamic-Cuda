"""
Main Integrator module
"""

import numpy as np

class INTEGRATOR(object):
    """
    Integrator base class
    """

    def __init__(self, dt, N):
        self.dt = dt
        self.N = N

    def first_step(self, x, v, a):
        return x, v

    def last_step(self, x, v, a):
        return x, v

