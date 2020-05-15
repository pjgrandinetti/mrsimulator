#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Potassium Sulfate
^^^^^^^^^^^^^^^^^

33S (I=3/2) quadrupolar line-shape simulation.
"""
# %%
# The following example is the :math:`^{33}\text{S}` NMR line-shape simulation of
# potassium sulfate (:math:`\text{K}_2\text{SO}_4`). The quadrupole tensor parameters
# for :math:`^{33}\text{S}` is obtained from Moudrakovski et. al. [#f3]_
import matplotlib.pyplot as plt
from mrsimulator import Isotopomer
from mrsimulator import Simulator
from mrsimulator import Site

#%%
# **Step 1** Create the sites, in this case, just the one.

S33 = Site(
    name="33S",
    isotope="33S",
    isotropic_chemical_shift=335.7,  # in ppm
    quadrupolar={"Cq": 0.959e6, "eta": 0.42},  # Cq is in Hz
)

#%%
# **Step 2** Create the isotopomer from the site.

isotopomer = Isotopomer(sites=[S33])

#%%
# **Step 3** Create a central transition selective Bloch decay spectrum method.

from mrsimulator.methods import BlochDecayCentralTransitionSpectrum

method = BlochDecayCentralTransitionSpectrum(
    channels=["33S"],
    magnetic_flux_density=21.14,  # in T
    rotor_frequency=14000,  # in Hz
    spectral_dimensions=[
        {
            "count": 2046,
            "spectral_width": 5000,  # in Hz
            "reference_offset": 22500,  # in Hz
        }
    ],
)


#%%
# **Step 4** Create the Simulator object and add the method and isotopomer object.

sim_K2SO3 = Simulator()
sim_K2SO3.isotopomers += [isotopomer]  # add isotopomer
sim_K2SO3.methods += [method]  # add method

#%%
# **Step 5** Simulate the spectrum.

sim_K2SO3.run()


#%%
# **Step 6** The plot of the simulation.

x, y = sim_K2SO3.methods[0].simulation.to_list()
plt.figure(figsize=(4, 3))
plt.plot(x, y, color="black", linewidth=1)
plt.xlabel("frequency / ppm")
plt.xlim(x.value.max(), x.value.min())
plt.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.show()

#%%
# .. [#f3] Moudrakovski, I., Lang, S., Patchkovskii, S., and Ripmeester, J. High field
#       :math:`^{33}\text{S}` solid state NMR and first-principles calculations in
#       potassium sulfates. J. Phys. Chem. A, 2010, **114**, *1*, 309–316.
#       `DOI: 10.1021/jp908206c <https://doi.org/10.1021/jp908206c>`_
