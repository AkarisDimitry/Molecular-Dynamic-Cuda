from INTERACTION import INTERACTION
import pyopencl as cl

class Friction(INTERACTION):
    """
    Base short-range class
    """
    def __init__(self, eta=0):
        self.eta = 0

    def make(self, context, N, boundary_max):
        # Load and build the OpenCL program
        #
        self.program = cl.Program(context, 
            open('Friction.cl').read().replace("eta", str(self.eta)) ).build()
        self.compute_forces = self.program.compute_forces
