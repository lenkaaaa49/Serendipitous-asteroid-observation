# Serendipitous-asteroid-observation
Code to determine the asteroids in a field of view of an instrument at a specific time. This is saved in MySQL database and using the information from Horizons, the expected brightness (thermal emission) of the asteroid is calculated as well.

This code takes an input from a MySQL input table. In Create_Dummy_Database.py such a table is created and can be used to run the whole code.

The neatm.py file is made by Migo Mueller. It is a wrap up around his function to calculate asteroid thermal emission following the Near-Earth Asteroid Thermal Model (NEATM, Harris 1998, http://dx.doi.org/10.1006/icar.1997.5865). Link to the code: https://github.com/MigoMueller/NEATM
The code calls on NEATM executable, which needs to be added to the path. The explanation to do this is given in the link above.
