"""
Main Integrator module
"""

import numpy as np

class BOUNDARY(object):
    """
    Integrator base class
    """

    def __init__(self, BC_type=None):
        self.BC_type = BC_type

