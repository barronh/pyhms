"""
HMS Smoke Plot
==============

This example shows how to create a plot from one day of HMS smoke."""


# %%
# Prepare a base api object
# -------------------------

# !python -m pip install git+https://github.com/barronh/pyhms.git
import pyhms

hms = pyhms.hmsapi()


# %%
# Define the date or dates
# ------------------------
date = '2023-06-14'
# date = pd.date_range('2023-07-01', '2023-07-31')

# %%
# Open one or many dates
# ----------------------
#
# * Implicitly calls download for date(s)
# * Then opens and concatenates
hmsf = hms.open(date)

# %%
# Create a plot with semi-transparent polgons
# -------------------------------------------
#
# * alpha controls transparency and is an example of adding keywords to the
#   plotting script that controls the polygons patches.
# * Note that with many dates, the plot is very busy.
# * By default, states are downloaded from the Census website and added to
#   the plot. To distable, add keyword statepath=None.
ax = pyhms.plot_smoke(hmsf, alpha=0.5)
ax.figure.savefig('HMS_smoke.png')