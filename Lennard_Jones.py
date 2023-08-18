from INTERACTION import INTERACTION
import pyopencl as cl

class Lennard_Jones(INTERACTION):
    """
    Base short-range class
    """
    def __init__(self, sigma=1, eps=1, rcut=10, shift_style='displace'):
        self.sigma = sigma
        self.eps = eps 
        self.rcut = rcut
        self.shift_style = shift_style

    def make(self, context, N, boundary_max):
        # Load and build the OpenCL program
        #

        self.program = cl.Program(context, 
            open('LJ.cl').read().replace("N", str(N)).replace("boundary_max", f'(float4)({boundary_max[0]}f, {boundary_max[1]}f, {boundary_max[2]}f, {boundary_max[3]}f)') 
            ).build()
        self.compute_forces = self.program.compute_forces
