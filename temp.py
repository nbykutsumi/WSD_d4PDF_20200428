# %%
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import d4PDF
from datetime import datetime, timedelta
from numpy import ma

expr = 'HPB_NAT'
ens  = 100
baseDir = '/home/utsumi/mnt/lab_work/hk02/BAMS.EEE.2020/test.HPB_NAT.m100'
cfg   ={'baseDir':baseDir}
dbsfc = d4PDF.snp_6hr_2byte(cfg,vtype='sfc')
dbatm = d4PDF.snp_6hr_2byte(cfg,vtype='atm')
DTime = datetime(2010,1,3,5)

lvname = ['height','ratiol']
#lvname = ['height']
#lvname = ['ratiol']
for vname in lvname:
    a2dat = dbatm.load_topo(vname=vname)
    print vname, a2dat.min(),a2dat.max(), a2dat.shape
    plt.imshow(a2dat, origin='lower')
    plt.title(vname)
    plt.colorbar()
    plt.show()

#lvname = ['SLP','UAOPN','TA','QA','PS','PRECIPI']
#for vname in lvname:
#    a2dat = dbsfc.load_6hr(vname, expr, ens, DTime)
#
#
#    print vname, a2dat.min(), a2dat.max(), type(a2dat)


#lvname = ['U850','U500','U300','V850','V500','V300','T850','T500','T300']
#for vname in lvname:
#    a2dat = dbatm.load_6hr(vname, expr, ens, DTime)
#    #plt.imshow(a2dat, origin='lower')
#    #plt.title(vname)
#    #plt.colorbar()
#    #plt.show()
#    print vname, a2dat.min(), a2dat.max()
# %%
#ny,nx = 320, 640
#nvar  = 7
#year,mon= 2010, 1
#baseDir = '/home/utsumi/mnt/lab_work/hk02/BAMS.EEE.2020/test.HPB_NAT.m100'
#srcDir  = baseDir + '/%04d%02d'%(year,mon)
#srcPath = srcDir + '/sfc_snp_6hr_2byte_HPB_NAT_m100_201001.dr'
#
#a4dat=np.fromfile(srcPath, 'int16').byteswap().reshape(-1,nvar,ny,nx)
#
#a,b =0.005, 273.15
#a2dat = a4dat[9,3,:,:] *a + b
#plt.imshow(a2dat, origin='lower')
#plt.colorbar()
#plt.show()
#
#
#a1dat = a4dat[100:120,3,50,50] *a + b
#plt.plot(a1dat)
#plt.show()
## %%
#

# %%
