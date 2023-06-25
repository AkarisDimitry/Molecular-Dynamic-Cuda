class INFILE(object):
    """
    This class holds the variables read from the input file
    """

    def __init__(self):

        # Initializing all the variables with None
        self.interaction_type = None
        self.interaction_rcut = None
        self.interaction_coef = []
        self.interaction_shift_style = None
        self.interaction_eps = None
        self.interaction_sigma = None

        self.integration_type = None
        self.integration_dt = None
        self.integration_N = None

        self.boxdata_type = None
        self.boxdata_min = None
        self.boxdata_max = None

        self.thermostat_type = None
        self.thermostat_coef = None
        self.thermostat_dt = None

    def parse_from_file(self, file_name):
        """
        This method reads the file and store the variables in the object
        """
        # Open file in read mode
        with open(file_name, "r") as file:
            for line in file:
                # Splitting line into key and value
                line = line.split("%")[0].strip()  # Removes any part of the line after a '%'
                if not line:  # Skips the line if it is empty
                    continue
                key, value = line.split(" = ")
                # If key is interaction_coef, it's a list
                # Setting the attribute of object with the value
                try: setattr(self, key, eval(value))
                except: setattr(self, key, value)
                
    def print(self, ):
      for key, item in list(self.__dict__.items()):
        print( f'{key:<30s}: {str(item):<20s} : {type(item)}')  # 👉️ ['first', 'last', 'age']

'''
# ===== EG/ ===== #
# Creating an object of class INFILE
infile = INFILE()

# Parsing the input file to store the variables in object
infile.parse_from_file("INFILE")
infile.print()
print(infile.interaction_type)
# ===== /EG ===== #

interaction_type  = flocking %  Coulomb, LJ
interaction_rcut  = 10.5
interaction_coef01  = [0,1,0]
interaction_coef02  = [0,-100,0]
interaction_coef03  = [0,-3,0]
interaction_shift_style  = Displace
interaction_eps  = Displace
interaction_sigma  = Displace
interaction_rcut  = Displace
interaction_rcut  = Displace
interaction_rcut  = Displace

integration_type = Velverlet
integration_dt = 0.05
integration_N = 2000

boxdata_type = Periodic
boxdata_min = [-0,-0,-0]
boxdata_max = [ 1.3*60, 1.3*60, 300]

thermostat_type = Friction 
thermostat_coef = 1.0 
thermostat_dt = 0.05 
'''