

Utilities
====================

This utility script calculates entropy production rate and exergy loss rates,
but specifically for adiabatic heat pumps or heat exchangers, only. It is
used by the heat_pump_simple.py script.

It is found at: carbatpy.utils.exergy_loss


.. automodule:: carbatpy.utils.exergy_loss
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    

.. automodule:: carbatpy.utils.curve_min_distance_finder
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    
Carnot Battery
===============

A simple Carnot battery run-script is found at carbatpy.utils.run_carnot_battery
which goes through the thermodynamics.
    
This can be used as a starting point for own scripts and variations.
The structure is for two double-tank storages, together with heat rejection 
to water at ambient temperature. Most of the script sets pressures,
temperature levels, fluid composition,
heat flow rates etc. The heat pump instance is hp0 and the ORC is orc0. Please check the
warnings at the end; only when both braclkets are empty,
there will be no crossing of temperature curves or too small
temperature differences. The final plot is found in the results directory
(resultslast_T_H_dot_plot_orc.png), but also further data are stored there. The directory
can be changed.

Helpers
====================

Some helper functions, found at carbatpy\\helpers
Here for copying all results and the source py-file to a new directory.


.. automodule:: carbatpy.helpers.file_copy
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members: