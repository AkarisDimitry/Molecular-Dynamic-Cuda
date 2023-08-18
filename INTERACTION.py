import numpy as np


class INTERACTION(object):
    """
    Base Interaction class.
    """
    def __init__(self, ):
        self.name = None

        self.platform = None
        self.device = None
        self.context = None
        self.queue = None

        # Create memory buffers
        self.mf = None
        self.positions_buf = None
        self.forces_buf = None

        # Load and build the OpenCL program
        self.program = None

        self.Bond = False
        self.Lennard_Jones = False
        self.Friction = False

    def load(self, ):
        pass