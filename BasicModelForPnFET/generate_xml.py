import openmc
import numpy as np
import matplotlib.pyplot as plt

### This is to generate xml
def generate_xml(ring_num,porder):
    fuelcell,total_fuel_cell=generate_mat_and_geom(ring_num)

#### THis is for material and geometry 
def generate_mat_and_geom(pln_num):    
    # 1.6 enriched fuel
    fuel = openmc.Material(name='1.6% Fuel')
    fuel.set_density('g/cm3', 10.31341)
    fuel.add_nuclide('U235', 3.7503e-4)
    fuel.add_nuclide('U238', 2.2625e-2)
    fuel.add_nuclide('O16', 4.6007e-2)
    # borated water
    water = openmc.Material(name='Borated Water')
    water.set_density('g/cm3', 0.740582)
    water.add_nuclide('H1', 4.9457e-2)
    water.add_nuclide('O16', 2.4732e-2)
    water.add_nuclide('B10', 8.0042e-6)
    # zircaloy
    zircaloy = openmc.Material(name='Zircaloy')
    zircaloy.set_density('g/cm3', 6.55)
    zircaloy.add_nuclide('Zr90', 7.2758e-3)

    # Instantiate a Materials collection
    materials_file = openmc.Materials([fuel, water, zircaloy])
    # Export to "materials.xml"
    materials_file.export_to_xml()

    # Create cylinders for the fuel and clad
    NumPln = pln_num
    fuel_radius =[]
    Rout = 0.392
    Cout = 0.457
    # darea = np.pi*Rout**2/NumRad
    # area = 0
    # Rlist = []
    # for i in range(0,NumRad):
    #     area += darea
    #     r = np.sqrt(area/np.pi)
    #     Rlist.append(r)
    #     fuel_radius.append(openmc.ZCylinder(x0=0.0, y0=0.0, R=r))

    clad_outer_radius = openmc.ZCylinder(x0=0.0, y0=0.0, R=Cout)
    fuel_outer_radius = openmc.ZCylinder(x0=0.0, y0=0.0, R=Rout)
    # Create a Universe to encapsulate a fuel pin
    min_x = openmc.XPlane(x0=-0.63, boundary_type='reflective')
    max_x = openmc.XPlane(x0=+0.63, boundary_type='reflective')
    min_y = openmc.YPlane(y0=-0.63, boundary_type='reflective')
    max_y = openmc.YPlane(y0=+0.63, boundary_type='reflective')
    min_z = openmc.ZPlane(z0=-100., boundary_type='vacuum')
    max_z = openmc.ZPlane(z0=+100., boundary_type='vacuum')

    zmin = -100
    zmax = 100
    dx = (zmax-zmin)/pln_num
    planes = []
    for i in range(1,NumPln):
        planes.append(openmc.ZPlane(z0=dx*i-100)) 
    # top = openmc.ZPlane(z0=zmax, boundary_type='reflective')

    fuelcelllist = []
    for i in range(0,len(planes)+1):
        if i == 0:
            fuel_cell = openmc.Cell(name='fuel',fill=fuel, region= -fuel_outer_radius & + min_z & - planes[0])
        elif i == pln_num-1:
            fuel_cell = openmc.Cell(name='fuel',fill=fuel, region= -fuel_outer_radius & + planes[pln_num-2] & - max_z)
        else :
            fuel_cell = openmc.Cell(name='fuel',fill=fuel, region= -fuel_outer_radius & + planes[i-1] & - planes[i])
        fuelcelllist.append(fuel_cell)

    fuel_cell_universe = openmc.Universe(name='Total Fuel Cell')
    for j in range(0,len(fuelcelllist)):
        fuel_cell_universe.add_cell(fuelcelllist[j])


    #Create total fuel cell
    total_fuel_cell = openmc.Cell(name='totalfuelcell')
    total_fuel_cell.fill = fuel_cell_universe
    total_fuel_cell.region = -fuel_outer_radius & +min_z & -max_z

    # Create a clad Cell
    clad_cell = openmc.Cell(name='1.6% Clad')
    clad_cell.fill = zircaloy
    clad_cell.region = +fuel_outer_radius & -clad_outer_radius & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

    # Create a moderator Cell
    moderator_cell = openmc.Cell(name='1.6% Moderator')
    moderator_cell.fill = water
    moderator_cell.region = +clad_outer_radius & +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

    # Create root Universe
    root_universe = openmc.Universe(universe_id=0, name='root universe')
    root_universe.add_cell(total_fuel_cell)
    root_universe.add_cell(moderator_cell)
    root_universe.add_cell(clad_cell)
    
    # Create Geometry and set root Universe
    geometry = openmc.Geometry(root_universe)
    
    # Export to "geometry.xml"
    geometry.export_to_xml()
    # openmc.plot_geometry(output=False)
    return fuelcelllist,total_fuel_cell

def generate_settings(N):
    # N is the active number of batches

    # OpenMC simulation parameters
    batches = N+100
    inactive = 100
    particles = 1000
    
    # Instantiate a Settings object
    settings_file = openmc.Settings()
    settings_file.batches = batches
    settings_file.inactive = inactive
    settings_file.particles = particles
    settings_file.output = {'tallies': True}
    
    # Create an initial uniform spatial source distribution over fissionable zones
    bounds = [-0.63, -0.63, -100., 0.63, 0.63, 100.]
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
    settings_file.source = openmc.source.Source(space=uniform_dist)
    
    # Export to "settings.xml"
    settings_file.export_to_xml()

def generate_tallies(fuelcelllist,total_fuel_cell,porder,flag):
    tallies_file = openmc.Tallies()
    cell_filter = openmc.CellFilter(fuelcelllist)
    total_fuel_cell_filter = openmc.CellFilter([total_fuel_cell])
    zmin = -100
    zmax = 100

    if flag == 1:
        # choose flag 1, we use tradiational estimators 
        tally3 = openmc.Tally(name='tracklength')
        tally3.filters.append(cell_filter)
        tally3.scores = ['nu-fission','absorption']
        tally3.nuclides = ['U238']
        tally3.estimator = 'tracklength'
        tallies_file.append(tally3)
        
        tally3 = openmc.Tally(name='collision')
        tally3.filters.append(cell_filter)
        tally3.scores = ['nu-fission','absorption']
        tally3.nuclides = ['U238']
        tally3.estimator = 'collision'
        tallies_file.append(tally3)
        
        tally3 = openmc.Tally(name='analog')
        tally3.filters.append(cell_filter)
        tally3.scores = ['nu-fission','absorption']
        tally3.nuclides = ['U238']
        tally3.estimator = 'analog'
        tallies_file.append(tally3)
    elif flag == 2:
        # we tally FET      
        str1 = 'fet'
        strorder = str(porder)
        name = str1+strorder
        fet_tally = openmc.Tally(name=name)
        fet_tally.filters.append(total_fuel_cell_filter)
        fet_tally.scores = ['nu-fission', 'absorption']
        fet_tally.nuclides = ['U238']
        expand_filter = openmc.SpatialLegendreFilter(porder, 'z', zmin, zmax)
        fet_tally.filters.append(expand_filter)
        tallies_file.append(fet_tally)

    tallies_file.export_to_xml()
