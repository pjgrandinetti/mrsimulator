#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ethanol Revisited (¹H and ¹³C NMR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simulating ¹H and ¹³C isotopomers.
"""
# %%
# An astute observer may have noticed that the :math:`^{1}\text{H}` ethanol spectrum
# from :ref:`getting_started_coupled_spin_system_etoh` was missing the characteristic
# :math:`^{13}\text{C}`
# `satellite peaks <https://en.wikipedia.org/wiki/Carbon-13_NMR_satellite>`_.
# In this example, we will add these to the :math:`^1\text{H}` spectrum and plot
# the :math:`^{13}\text{C}` spectrum while we're at it!
#
# As before, we start by importing the necessary packages.
import matplotlib.pyplot as plt

from mrsimulator import Simulator, SpinSystem, Site, Coupling
from mrsimulator.methods import BlochDecaySpectrum
from mrsimulator import signal_processing as sp

# sphinx_gallery_thumbnail_number = 1

# %%
# Spin Systems
# ------------
#
# The satellite peaks come from couplings between :math:`^{1}\text{H}` and
# :math:`^{13}\text{C}` in low-abundance isotopomers. First, let's define
# all the possible :math:`^1\text{H}` and :math:`^{13}\text{C}` sites.

H_CH3 = Site(isotope="1H", isotropic_chemical_shift=1.226)
H_CH2 = Site(isotope="1H", isotropic_chemical_shift=2.61)
H_OH = Site(isotope="1H", isotropic_chemical_shift=3.687)

C_CH3 = Site(isotope="13C", isotropic_chemical_shift=18)
C_CH2 = Site(isotope="13C", isotropic_chemical_shift=58)

# %%
# **Isotopomer 1**
#
# Now, let's define the couplings and build the spin system for the most abundant
# isotopomer (pictured below).
#
# .. figure::  ../../_static/iso1.*
#     :width: 200
#     :alt: figure
#     :align: center
#
#     An isotopomer of ethanol containing all :math:`^{1}\text{H}` and all
#     :math:`^{12}\text{C}` isotopes.
#
iso1_sites = [H_CH3, H_CH3, H_CH3, H_CH2, H_CH2, H_OH]

HH_coupling_1 = Coupling(site_index=[0, 3], isotropic_j=7)
HH_coupling_2 = Coupling(site_index=[0, 4], isotropic_j=7)
HH_coupling_3 = Coupling(site_index=[1, 3], isotropic_j=7)
HH_coupling_4 = Coupling(site_index=[1, 4], isotropic_j=7)
HH_coupling_5 = Coupling(site_index=[2, 3], isotropic_j=7)
HH_coupling_6 = Coupling(site_index=[2, 4], isotropic_j=7)

iso1_couplings = [
    HH_coupling_1,
    HH_coupling_2,
    HH_coupling_3,
    HH_coupling_4,
    HH_coupling_5,
    HH_coupling_6,
]

isotopomer1 = SpinSystem(sites=iso1_sites, couplings=iso1_couplings, abundance=97.812)

# %%
# .. note::
#     The abundance values were calculated with an assumption that only
#     :math:`^1\text{H}` and :math:`^{16}\text{O}` are present.  The abundance
#     of :math:`^{12}\text{C}` is 98.9%, and the abundance of :math:`^{13}\text{C}`
#     is 1.1%. So, the probability of the most abundant isotopomer is
#     :math:`0.989 \times 0.989=0.97812`
#
# **Isotopomer 2**
#
# Now, we build the sites, couplings (:math:`^1J_\text{CH}` and
# :math:`^3J_\text{HH}`), and spin system for the isotopomer with the
# methyl carbon replaced with a :math:`^{13}\text{C}` (pictured below,
# :math:`^{13}\text{C}` marked in blue)
#
# .. figure::  ../../_static/iso2.*
#     :width: 200
#     :alt: figure
#     :align: center
#
#     Second isotopomer of ethanol containing all :math:`^{1}\text{H}`,
#     :math:`^{13}\text{C}` methyl, and :math:`^{12}\text{C}` methylene isotopes.

iso2_sites = [H_CH3, H_CH3, H_CH3, H_CH2, H_CH2, H_OH, C_CH3]

CH3_coupling_1 = Coupling(site_index=[0, 6], isotropic_j=125)
CH3_coupling_2 = Coupling(site_index=[1, 6], isotropic_j=125)
CH3_coupling_3 = Coupling(site_index=[2, 6], isotropic_j=125)

iso2_couplings = iso1_couplings + [CH3_coupling_1, CH3_coupling_2, CH3_coupling_3]

isotopomer2 = SpinSystem(sites=iso2_sites, couplings=iso2_couplings, abundance=1.088)

# %%
# **Isotopomer 3**
#
# Lastly, we build the sites, couplings, and spin system for the other
# isotopomer with the methylene carbon replaced with :math:`^{13}\text{C}` (pictured
# below, :math:`^{13}\text{C}` marked in blue)
#
# .. figure::  ../../_static/iso3.*
#     :width: 200
#     :alt: figure
#     :align: center
#
#     Third isotopomer of ethanol containing all :math:`^{1}\text{H}`,
#     :math:`^{12}\text{C}` methyl, and :math:`^{13}\text{C}` methylene isotopes.

iso3_sites = [H_CH3, H_CH3, H_CH3, H_CH2, H_CH2, H_OH, C_CH2]

CH2_coupling_1 = Coupling(site_index=[3, 6], isotropic_j=141)
CH2_coupling_2 = Coupling(site_index=[4, 6], isotropic_j=141)

iso3_couplings = iso1_couplings + [CH2_coupling_1, CH2_coupling_2]

isotopomer3 = SpinSystem(sites=iso3_sites, couplings=iso3_couplings, abundance=1.088)

# %%
# Methods
# -------
#
# Now, we define simple 1 pulse-acquire methods for both :math:`^1\text{H}` and
# :math:`^{13}\text{C}`.
method_H = BlochDecaySpectrum(
    channels=["1H"],
    magnetic_flux_density=9.4,  # T
    spectral_dimensions=[
        {
            "count": 16000,
            "spectral_width": 1.5e3,
            "reference_offset": 950,
            "label": "$^{1}$H frequency",
        }
    ],
)

method_C = BlochDecaySpectrum(
    channels=["13C"],
    magnetic_flux_density=9.4,  # T
    spectral_dimensions=[
        {
            "count": 32000,
            "spectral_width": 8e3,
            "reference_offset": 4e3,
            "label": "$^{13}$C frequency",
        }
    ],
)

# %%
# Simulation
# ----------
#
# Now, we create an instance of the simulator object, add our three spin
# systems, add our two methods, and run the simulation.
spin_systems = [isotopomer1, isotopomer2, isotopomer3]
methods = [method_H, method_C]
sim = Simulator(spin_systems=spin_systems, methods=methods)
sim.run()

# %%
# Let's set up our post-simulation processing.
processor_1H = sp.SignalProcessor(
    operations=[
        sp.IFFT(),
        sp.apodization.Exponential(FWHM="1 Hz"),
        sp.FFT(),
    ]
)

processor_13C = sp.SignalProcessor(
    operations=[
        sp.IFFT(),
        sp.apodization.Exponential(FWHM="20 Hz"),
        sp.FFT(),
    ]
)

# %%
# Now, let's get our two datasets out of the simulation object and apply the
# post-processing.
H_data = sim.methods[0].simulation
C_data = sim.methods[1].simulation

processed_H_data = processor_1H.apply_operations(data=H_data)
processed_C_data = processor_13C.apply_operations(data=C_data)

# %%
# Lastly, we plot the two spectra.
fig, ax = plt.subplots(
    nrows=1, ncols=2, subplot_kw={"projection": "csdm"}, figsize=[8, 3.5]
)

ax[0].plot(processed_H_data.real, color="black", linewidth=0.5)
ax[0].invert_xaxis()
ax[0].set_title("$^1$H")

ax[1].plot(processed_C_data.real, color="black", linewidth=0.5)
ax[1].invert_xaxis()
ax[1].set_title("$^{13}$C")

plt.tight_layout()
plt.show()

# %%
# Now, we see the :math:`^{13}\text{C}` satellites on either side of the peaks near
# 1.2 ppm and 2.6 ppm in the :math:`^1\text{H}` spectrum.
