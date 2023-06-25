"""
Main Thermostat module.
"""

import numpy as np


class THERMOSTAT(object):
  """
  Thermostat base class
  """
  def __init__(self, name=None, dt=None, coef=None):
    self.dt = dt
    self.name = name
    self.coef = coef
    self.idn = None
    self.v = None

  def E_disp(self, x, v, a):
    return None

  def E_tot(self, x, v, a):
    return None

class ClassicMechanics(THERMOSTAT):
  """
  ClassicMechanics class
  """

class FriccionCoef(THERMOSTAT):
  """
  Friccion Coef Thermostat
  """
  def friction(self, dt=None, v=None, coef=None):
    if coef == None:  coef = float(self.coef)
    if dt == None:    dt = float(self.dt)
    if not type(v) is np.ndarray:      v = float(self.v)

    v = v*coef

    return v


