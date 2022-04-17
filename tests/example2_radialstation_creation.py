import propeller_design_tools as pdt


pdt.set_airfoil_database(r'C:\Users\Jake\Desktop\Python Projects\propeller_design_tools\propeller_design_tools\foil_database')

af = pdt.Airfoil('clarky')
rs = pdt.RadialStation(foil=af, re_estimate=5500000, plot=True)
