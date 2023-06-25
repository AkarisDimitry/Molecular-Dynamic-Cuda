import INFILE, POSFILE
import pyopencl as cl

from THERMOSTAT import *
from INTERACTION import *
from Lennard_Jones import *
from VelVerlet import *
from BOUNDARY import *
from Periodic import *

class SIMULATION(object):

    def __init__(self, ):

        self.verbosity = True

        self.POSFILE = None
        self.OUTFILE = None
        self.INFILE = None

        self.sistema = None
        self.interaction = None
        self.integrator = None
        self.boundary = None
        self.thermostat = None
        self.step, self.steps = None, None

        self.save = True

    def run(self, ):
        # Create OpenCL context and command queue
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)

        # Create device memory
        self.mf = cl.mem_flags

        self.interaction.make(  context =    self.context, 
                                    N   =    self.POSFILE.N)
        self.integrator.make(  context  =    self.context, )
        self.POSFILE.make(  context     =    self.context, 
                                mf      =    self.mf)
        self.boundary.make(  context    =    self.context , 
                                mf      =    self.mf)

        self.POSFILE.store_data['x'] = np.zeros(( int(self.integrator.N/self.POSFILE.store_data['step']), self.POSFILE.N, 4), dtype=np.float32)

        # Main simulation loop
        for step in range(self.integrator.N):
            # Compute the forces

            self.interaction.compute_forces(self.queue, (self.POSFILE.N,), None, self.POSFILE.d_positions, self.POSFILE.d_forces)
            self.integrator.integrate_step1(self.queue, (self.POSFILE.N,), None, self.POSFILE.d_positions, self.POSFILE.d_velocities, self.POSFILE.d_forces)
            
            if step % self.boundary.step == 0:
                self.boundary.boundary(self.queue, (self.POSFILE.N,), None, self.POSFILE.d_positions, self.POSFILE.d_velocities, self.boundary.boundary_min, self.boundary.boundary_max, self.boundary.L )

            self.interaction.compute_forces(self.queue, (self.POSFILE.N,), None, self.POSFILE.d_positions, self.POSFILE.d_forces)
            self.integrator.integrate_step2(self.queue, (self.POSFILE.N,), None, self.POSFILE.d_positions, self.POSFILE.d_velocities, self.POSFILE.d_forces)

            if step % self.POSFILE.store_data['step'] == 0:
                print(f"Completed step {step}")
                cl.enqueue_copy(self.queue, self.POSFILE.positions, self.POSFILE.d_positions)
                #cl.enqueue_copy(self.queue, self.POSFILE.forces, self.POSFILE.d_forces)
                self.POSFILE.store_data['x'][int(step/self.POSFILE.store_data['step']),:,:] = self.POSFILE.positions
            
        self.POSFILE.save_OUTFILE('OUTFILE')

    def load_thermostat(self, thermostat_type=None, coef=None, dt=None):
        if thermostat_type == 'Friction':
            self.thermostat = FriccionCoef(coef=coef, dt=dt)

        return True

    def load_interaction(self, interaction_type=None):
        if interaction_type == 'LJ':
            self.interaction = Lennard_Jones()
            
        return True

    def load_integration(self, integration_type=None, integration_dt=None, integration_N=None):
        if integration_type == 'Velverlet':
            self.integrator = VelVerlet(    dt=integration_dt, 
                                            N=integration_N )
        return True

    def load_boundary(self, boundary_type=None, boundary_min=None, boundary_max=None, boundary_step=None):
        if boundary_type == 'Periodic':
            self.boundary = Periodic(   boundary_min=boundary_min, 
                                        boundary_max=boundary_max, 
                                        boundary_type=boundary_type,
                                        boundary_step=boundary_step )

        return True


    def load_INFILE(self, file:str=None,  verbosity:bool=None):
        verbosity = verbosity if type(verbosity) is bool else self.verbosity 

        # Creating an object of class INFILE
        infile = INFILE.INFILE()

        # Parsing the input file to store the variables in object
        infile.parse_from_file(str(file))
        if verbosity: infile.print()

        self.INFILE = infile

        # ---- THERMOSTAT ---- #
        self.load_thermostat(   thermostat_type = self.INFILE.thermostat_type,
                                coef = self.INFILE.thermostat_coef,
                                dt = self.INFILE.thermostat_dt, )

        # ---- INTERACTION ---- #
        self.load_interaction( self.INFILE.interaction_type )

        # ---- INTEGRATION ---- #
        self.load_integration(  integration_type = self.INFILE.integration_type, 
                                integration_dt   = self.INFILE.integration_dt, 
                                integration_N    = self.INFILE.integration_N, )

        # ---- BOX ---- #
        self.load_boundary(  boundary_type= self.INFILE.boundary_type, 
                             boundary_min = self.INFILE.boundary_min, 
                             boundary_max = self.INFILE.boundary_max, )


        return True

    def load_POSFILE(self, file:str=None,  verbosity:bool=None):
        verbosity = verbosity if type(verbosity) is bool else self.verbosity 

        posfile = POSFILE.POSFILE()
        posfile.load('POSFILE')
        if verbosity: posfile.print()
        
        self.POSFILE = posfile

        return True

    def load(self, path:str, verbosity:bool=None) -> bool:
        verbosity = verbosity if type(verbosity) is bool else self.verbosity 

        self.load_INFILE(file=path+'INFILE')
        self.load_POSFILE(file=path+'POSFILE')

        return True

sim = SIMULATION()
sim.load('./')
sim.run()

