
Components evaluation
=========================

A very basic approach to calculate heat exchangers, compressores(and expanders) 
as well as throttles.

Heat exchangers
---------------
Simple heat exchangers, only thermodynamic balances are calculated (no UA),
and by varying the mass flow rate and one state-point (temperature), a
minimum approach temperature is satisfied, but only if the given restrictions
allow it.
   
.. automodule:: carbatpy.models.components.heat_exchanger_thermo_v2
    :members:
    :special-members: __init__ 
    :undoc-members:
    :show-inheritance:

Compressors and Expanders
-------------------------

According to the given pressure levels, the script decides,
whether it is a compressor or an expander. At the moment the 
isentropic efficiency must be provided.

.. automodule:: carbatpy.models.components.compressor_simple
    :members:
    :special-members: __init__ 
    :undoc-members:
    :show-inheritance:

Throttle
-------------
For isenthalpic throttles only.

.. automodule:: carbatpy.models.components.throttle_simple
    :members:
    :special-members: __init__ 
    :undoc-members:
    :show-inheritance:
    
Mixing Chamber (Flow Device)
----------------------------
For mixing two streams.


.. automodule:: carbatpy.models.components.flow_devices
    :members:
    :special-members: __init__ 
    :undoc-members:
    :show-inheritance: