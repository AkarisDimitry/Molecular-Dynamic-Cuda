from BOUNDARY import BOUNDARY
import numpy as np
import pyopencl as cl

class Periodic(BOUNDARY):
    """
    Box class
    """
    def __init__(self, boundary_min=np.array([0,0,0,0]), boundary_max=None, boundary_type='Periodic', boundary_step=100):
        """
        Parameters
        ----------

        boundary_min : NumPy array
            Initial vertex of the box

        boundary_max : NumPy array
            Final vertex of the box

        boundary_type : {'Periodic', 'Fixed', 'Fixed Bounce'}
            Type of boundary
        """
        self.boundary_max = np.array(boundary_max).astype(np.float32) 
        self.boundary_min = np.array(boundary_min).astype(np.float32) 
        self.L = np.array(boundary_max) -  np.array(boundary_min)
        self.step = boundary_step if not boundary_step is None else 100
        self.boundary_type = boundary_type

    def make(self, context, mf):
        # Load and build the OpenCL program
        self.boundary_min = np.array(self.boundary_min, dtype=np.float32)
        self.boundary_max = np.array(self.boundary_max, dtype=np.float32)
        self.L = np.array(self.L, dtype=np.float32)

        self.d_boundary_min = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.boundary_min)
        self.d_boundary_max = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.boundary_max)
        self.d_L = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.L)

        self.program = cl.Program(context, open('Periodic.cl').read() ).build()
        self.boundary = self.program.Periodic

