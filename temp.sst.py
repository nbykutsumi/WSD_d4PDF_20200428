# %%
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pygrib
import os, sys
%matplotlib inline

srcdir = '/home/utsumi/bin/detect_bams2020/test.HPB_NAT.m100/201001'
srcpath= srcdir + '/sfc_souseid_avr_day_HPB_NAT_m100_201001.grib'

grbs = pygrib.open(srcpath)
grbs.seek(0)
#for grb in grbs[:25]:
#    grb = grbs.read(1)
#    print grb

grb = grbs.select(indicatorOfParameter=255)
data = grb[0].values
print ''
print data
plt.imshow(data,origin='lower')
plt.colorbar()
#data = grbs.select(name='TMPGRD')
#print data


# %%
e