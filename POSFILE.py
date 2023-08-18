import numpy as np
import pyopencl as cl

class POSFILE(object):
    def __init__(self, file_name=None, name=None, atoms=None, atoms_list=None):
        self.name = name
        self.path = None
        self.file_name = file_name

        self.N = None                   # N total number of atoms :: len(self.atoms)
        self.scale = None               # scale factor
        self.selective_dynamics = None  # selective dynamics" feature  :: (bool)

        self.position = atoms              # np.array(3,N)
        self.atoms_number = None        # [n(Fe), n(N), n(C), n(H) ]

        self.contrains = None
        
        self.atoms_names_list = None    # [Fe, N, N, N, N, C, C, C, C, H]
        self.atoms_names_ID = None      # [Fe, N, C, H] 
        self.atoms_names_full = None    # FeFeFeNNNNNNNCCCCCCCCCCCCCCCHHHHHHHHHHHHHHHH

        self.cell = None                # 3x3 [a1,a2,a3]
        self.distances = None           # distance matrix

        self._b = None # vectores propios de la red resiproca
        self._a = None # vectores propios de la red directa

        self.store_data = { 'x':  None,
                            'v':  None,
                            'f':  None,
                            'Ep': None,
                            'Ec': None,
                            'step':100,}

        self.plot_color = [
            '#DC143C', #    crimson             #DC143C     (220,20,60)
            '#ADFF2F', #    green yellow        #ADFF2F     (173,255,47)
            '#40E0D0', #    turquoise           #40E0D0     (64,224,208)
            '#FF8C00', #    dark orange         #FF8C00     (255,140,0)
            '#BA55D3', #    medium orchid       #BA55D3     (186,85,211)
            '#1E90FF', #    dodger blue         #1E90FF     (30,144,255)
            '#FF1493', #    deep pink           #FF1493     (255,20,147)
            '#8B4513', #    saddle brown        #8B4513     (139,69,19)
            '#FFD700', #    gold                #FFD700     (255,215,0)
            '#808000', #    Olive               #808000     (128,128,0)
            '#808080', #    Gray                #808080     (128,128,128)
            '#FF00FF', #    Magenta / Fuchsia   #FF00FF     (255,0,255)
            '#00FFFF', #    Cyan / Aqua         #00FFFF     (0,255,255)
            '#000000', #    Black               #000000     (0,0,0)
                                    ] 

        self.atomic_mass = {
    'H': 1.008,    'He': 4.0026,    'Li': 6.94,    'Be': 9.0122,
    'B': 10.81,    'C': 12.01,    'N': 14.01,    'O': 16.00,
    'F': 19.00,    'Ne': 20.18,    'Na': 22.99,    'Mg': 24.31,
    'Al': 26.98,    'Si': 28.09,    'P': 30.97,    'S': 32.07,
    'Cl': 35.45,    'Ar': 39.95,    'K': 39.10,    'Ca': 40.08,
    'Sc': 44.96,    'Ti': 47.87,    'V': 50.94,    'Cr': 52.00,
    'Mn': 54.94,    'Fe': 55.85,    'Ni': 58.69,    'Co': 58.93,
    'Cu': 63.55,    'Zn': 65.38,    'Ga': 69.72,    'Ge': 72.63,
    'As': 74.92,    'Se': 78.97,    'Br': 79.90,    'Kr': 83.80,
    'Rb': 85.47,    'Sr': 87.62,    'Y': 88.91,    'Zr': 91.22,
    'Nb': 92.91,    'Mo': 95.95,    'Tc': 98.00,    'Ru': 101.1,
    'Rh': 102.9,    'Pd': 106.4,    'Ag': 107.9,    'Cd': 112.4,
    'In': 114.8,    'Sn': 118.7,    'Sb': 121.8,    'I': 126.9,
    'Te': 127.6,    'Xe': 131.3,    'Cs': 132.9,    'Ba': 137.3,
    'La': 138.9,    'Ce': 140.1,    'Pr': 140.9,    'Nd': 144.2,
    'Pm': 145.0,    'Sm': 150.4,    'Eu': 152.0,    'Gd': 157.3,
    'Tb': 158.9,    'Dy': 162.5,    'Ho': 164.9,    'Er': 167.3,
    'Tm': 168.9,    'Yb': 173.0,    'Lu': 175.0,    'Hf': 178.5,
    'Ta': 180.9,    'W': 183.8,    'Re': 186.2,    'Os': 190.2,
    'Ir': 192.2,    'Pt': 195.1,    'Au': 197.0,    'Hg': 200.6,
    'Tl': 204.4,    'Pb': 207.2,    'Bi': 208.9,    'Th': 232.0,
    'Pa': 231.0,    'U': 238.0,    'Np': 237.0,    'Pu': 244.0,
    'Am': 243.0,    'Cm': 247.0,    'Bk': 247.0,    'Cf': 251.0,
    'Es': 252.0,    'Fm': 257.0,    'Md': 258.0,    'No': 259.0,
    'Lr': 262.0
}

    def load(self, file_name:str=None, save:bool=True) -> list:
        if file_name is None:   file_name = self.file_name

        # ------------------------ LOAD data from POSCAR ------------------------ #
        # name              :   STR     :   path+name of file to load 
        # ------------------------------- #     # ------------------------------- #
        # atom_name         :   LIST    :   List with all atoms names with-out repeat
        # atom_numbers      :   LIST    :   List with the number of atoms of each specie
        # atom_position     :   LIST    :   contains XYZ data from all atoms divided by species
        # position  :   N-MAT   :   Numpy array with all XYZ data
        # cell              :   N-MAT   :   Numpy array with cell parameters
        # N                 :   INT     :   Integer with total number of atoms
        # ------------------------------- #    # ------------------------------- #

        try:    f = open(file_name,'r')
        except:     print('ERROR :: POSCAR.load() :: missing file {}'.format(file_name) );  return
        # variables preset #
        cell                = np.zeros((3,3)) 
        N                   = 0 
        
        position               = []
        atoms_number        = [] 

        atoms_names_list    = [] 
        atoms_names_ID      = [] 
        atoms_names_full    = ''

        selective_dynamics  = False
        direct              = 0
        scale               = 0
        contrains           = []

        shift = 0 # shift the pointe depending on explicit POSCAR variables. eg. selective_dinamics

        for i, n in enumerate(f):
            vec = [m for m in n.replace('\t',' ').split(' ') if m != '' and m != '\n']
            try: 
                if vec[-1][-1:] == '\n': vec[-1] = vec[-1][:-1]
            except: pass

            # **** LOAD SCALE FACTOR**** #
            if i == 1: scale = float(vec[0])

            # **** LOAD CELL **** #
            for m in range(3):
                if i == 2+m:  cell[m,0]=float(vec[0]);  cell[m,1]=float(vec[1]); cell[m,2]=float(vec[2])

            # **** LOAD ATOMS names (without repetition) **** #
            if i == 5:
                for m in vec: atoms_names_ID.append(m)

            # **** LOAD ATOMS names (with repetition) **** #
            if i == 6:
                for j, m in enumerate(vec):  
                    N += int(m);                                    # total number of atoms
                    atoms_number.append( int(m) );                      # number of each specie
                    atoms_names_full += str(atoms_names_ID[j])*int(m)
                    atoms_names_list += [atoms_names_ID[j]]*int(m)
                position = np.zeros((N, 3))

            # **** Selective dynamics (optional) **** # 
            '''
            if the line after the "Ions per species" section contains Selective dynamics it enables the "selective dynamics" 
            feature (actually only the first character is relevant and must be S or s). This allows to provide extra flags
            for each atom signaling whether the respective coordinate(s) of this atom will be allowed to change during the 
            ionic relaxation. This setting is useful if only certain shells around a defect or layers near a surface should
            relax. See also the IBRION tag. 
            '''
            if   i == 7 and vec[0]=='Selective':        selective_dynamics = True; 
            elif i == 7 and not vec[0]=='Selective':    selective_dynamics = False; shift+=1

            # **** LOAD ATOMS positions **** #  
            if i == 8-shift and vec[0]=='Direct':       direct = True
            elif i == 8-shift and not vec[0]=='Direct': direct = False

            # **** LOAD ATOMS contrains **** #  
            if i >= 9-shift:
                if i < N+9-shift: 
                    position[i-9+shift,:] = np.array( [vec[0], vec[1], vec[2]] )
                    if len(vec) > 4:    contrains.append([True if 'T' in n else False for n in [vec[3], vec[4], vec[5]]] )
                    else:               contrains.append([True, True, True])

        # close the file 
        try:        f.close()
        except:     print('ERROR :: POSCAR.load() :: can NOT close file {}'.format(file_name) );    return

        # ---- store loaded data in OBJ ---- #

        if save:
            self.cell               = np.array(cell)
            self.N                  = N
            self.scale              = scale
            self.selective_dynamics = selective_dynamics

            self.position           = np.array(position).astype(np.float32)
            self.velocities         = np.zeros_like(position).astype(np.float32)
            self.forces             = np.empty_like(position).astype(np.float32)
            self.atoms_number       = atoms_number

            self.contrains          = contrains

            self.atoms_names_list       = atoms_names_list
            self.atoms_names_full   = atoms_names_full
            self.atoms_names_ID     = atoms_names_ID

            self.masses = np.array([ self.atomic_mass[n] for n in self.atoms_names_list ]).astype(np.float32)

            if direct:  self.coordenate = 'Direct'
            else:       self.coordenate = 'Cartesian'
        
        self.direct_to_cartesian()
        return  np.array(cell), N, np.array(position), atoms_number,  contrains, atoms_names_list, atoms_names_full, atoms_names_ID

    def make(self, context, mf):
        self.positions = np.c_[self.position, np.zeros(self.position.shape[0])].astype(np.float32) 
        self.velocities = np.zeros_like(self.positions).astype(np.float32) 
        self.forces = np.zeros_like(self.positions).astype(np.float32) 
        self.masses = self.masses.astype(np.float32) 

        # Create OpenCL context and command queue
        #self.context = cl.create_some_context()
        #self.queue = cl.CommandQueue(context)

        # Create device memory
        self.d_positions    = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.positions)
        self.d_velocities   = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.velocities)
        self.d_forces       = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.forces)
        self.d_masses       = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=self.masses)


    def direct_to_cartesian(self, position=None, cell=None, save=True, force=False, criteria=False, v=True):
        if not type(position) == np.ndarray:   position = self.position
        elif type(position) == list:           position = np.array(position)

        if not type(cell) == np.ndarray:    cell = self.cell
        elif type(cell) == list:            cell = np.array(cell)

        criteria = True if (position<= 1.0).all()  else False

        if self.coordenate == 'Direct' or force or criteria:
            try:
                position = np.dot(position, cell) 
            except: 
                if v: print('ERROR :: POSCAR.direct_to_cartesian() :: can not convert direct to cartesian' )
                return

            if save: self.position = position
            self.coordenate = 'Cartesian'
        else:
            pass
            #if v: print('WARNNING :: POSCAR.direct_to_cartesian() :: can not convert direct to cartesian' )

        return position
        
    def print(self, ):
      for key, item in list(self.__dict__.items()):
        print( f'{key:<30s}: {str(item):<20s} : {type(item)}')  # 👉️ ['first', 'last', 'age']


    def save_OUTFILE(self, file_name):
        file = open(file_name, 'w')
        for i, step in enumerate(self.store_data['x']):
            file.write( '{} \n'.format(int(self.N)) )
            file.write( ' TIme: {} fs -- step count: {} \n'.format(i, i) )
            for j, atom in enumerate(step):
                file.write( '{} \t {} \t {} \t {} 10 0 0 \n'.format(self.atoms_names_list[j], float(atom[0]), float(atom[1]), float(atom[2])) )
           
'''
posfile = POSFILE()
posfile.load('POSFILE')
posfile.print()
'''