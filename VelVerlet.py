from INTEGRATOR import INTEGRATOR
import pyopencl as cl

class VelVerlet(INTEGRATOR):
    """
    Velocity Verlet Integrator
    """
    def first_step(self, x, v, a, constrain):
        x[constrain==1] = x[constrain==1] + v[constrain==1]*self.dt + 0.5*a[constrain==1]*self.dt**2
        v[constrain==1] = v[constrain==1] + 0.5*a[constrain==1]*self.dt
        return x, v

    def make(self, context, ):
        self.program = cl.Program(context, open('VelVerlet.cl').read().replace("dt", str(self.dt)) ).build()
        self.integrate_step1 = self.program.integrate_step1
        self.integrate_step2 = self.program.integrate_step2

        return True  

    def last_step(self, x, v, a, constrain):
        v[constrain==1] = v[constrain==1] + 0.5*a[constrain==1]*self.dt
        return x, v