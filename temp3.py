# %%
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
%matplotlib inline


#srcpath = '/home/utsumi/mnt/lab_tank/utsumi/bams2020/6hr/pgrad/2010/01/pgrad.2010010418.320x640'
#srcpath = '/home/utsumi/mnt/lab_tank/utsumi/bams2020/6hr/vortlw/2010/01/vortlw.2010010418.320x640'
srcpath = '/home/utsumi/mnt/lab_tank/utsumi/bams2020/run.mean/va/2010/01/run.mean.va.0500hPa.2010010300.320x640'
a=ma.masked_equal(np.fromfile(srcpath, 'float32').reshape(320,640),-9999.)
plt.imshow(a,origin='lower')
plt.colorbar()
plt.show()

# %%
