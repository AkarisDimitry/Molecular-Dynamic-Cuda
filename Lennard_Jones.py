from INTERACTION import INTERACTION
import pyopencl as cl

class Lennard_Jones(INTERACTION):
    """
    Base short-range class
    """
    def __init__(self, ):
        pass

    def make(self, context, N):
        # Load and build the OpenCL program
        self.program = cl.Program(context, open('LJ.cl').read().replace("N", str(N)) ).build()
        self.compute_forces = self.program.compute_forces
