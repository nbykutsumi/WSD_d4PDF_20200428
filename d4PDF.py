import os, sys
import numpy as np
import struct
from numpy import ma
from datetime import datetime, timedelta
from collections import OrderedDict as odict


class snp_6hr_2byte(object):
    def __init__(self, cfg, vtype=None):
        self.baseDir = cfg['databaseDir']
        self.vtype   = vtype
        self.nvar    = {'sfc':7, 'atm':14}[vtype]
        self.miss_in = -32768
        self.miss_out= -9999.
        self.ny      = 320
        self.nx      = 640
        self.Lon     = Lon()
        self.Lat     = Lat()

        self.fmtsize = self.nvar*self.ny*self.nx*2 # bytes

        if vtype=='sfc':
            dictvars = odict([
                        ('SLP',     [1.0    ,100000]),  # Pa
                        ('UAOPN',   [0.01   ,0.0   ]),  # m/s
                        ('VAOPN',   [0.01   ,0.0   ]),  # m/s
                        ('TA',      [0.005  ,273.15]),  # K
                        ('QA',      [1.0e-6 ,2.0e-2]),  # kg/kg
                        ('PS',      [1.0    ,75000 ]),  # Pa
                        ('PRECIPI', [1.0e-6 ,0.03  ]),  # kg/m**2/s
                        ])
        else:
            dictvars = odict([
                        ('U850',    [0.01   ,0.0   ]),  # m/s
                        ('U700',    [0.01   ,0.0   ]),  # m/s
                        ('U500',    [0.01   ,0.0   ]),  # m/s
                        ('U300',    [0.01   ,0.0   ]),  # m/s
                        ('V850',    [0.01   ,0.0   ]),  # m/s
                        ('V700',    [0.01   ,0.0   ]),  # m/s
                        ('V500',    [0.01   ,0.0   ]),  # m/s
                        ('V300',    [0.01   ,0.0   ]),  # m/s
                        ('T850',    [0.005  ,273.15]),  # K
                        ('T700',    [0.005  ,273.15]),  # K
                        ('T500',    [0.005  ,273.15]),  # K
                        ('T300',    [0.005  ,273.15]),  # K
                        ('OMG700',  [0.001  ,0.0   ]),  # Pa/s
                        ('OMG500',  [0.001  ,0.0   ]),  # Pa/s
                        ])
        self.vars, \
        self.coefs   = zip(*dictvars.items())
        self.dictvars= dictvars

    def load_6hr(self, vname,scen,ens,DTime):
        Year,Mon = DTime.timetuple()[:2]
        srcDir  = self.baseDir + '/%02d%02d'%(Year,Mon)
        srcPath = srcDir + '/%s_snp_6hr_2byte_%s_m%03d_%04d%02d.dr'%(self.vtype,scen, ens,Year,Mon)

        ny,nx,nvar = self.ny, self.nx, self.nvar
        nsteps     = os.stat( srcPath ).st_size / (ny*nx*nvar*2) # num of timesteps
        mmap   = np.memmap( srcPath, dtype='int16', mode='r'
                           ,shape=(nsteps, nvar, ny, nx))

        vidx   = self.vars.index(vname)
        a,b    = self.coefs[vidx]
        istep  = int((DTime - datetime(Year,Mon,1,0)).total_seconds() \
                                                /(3600*6))
        data   = ma.masked_equal(np.array( mmap[istep, vidx, :, :] ).byteswap(), self.miss_in)*a + b
        return data

    def load_ave_mon(self, vname, scen, ens, Year, Mon):
        srcDir  = self.baseDir + '/%02d%02d'%(Year,Mon)
        srcPath = srcDir + '/%s_snp_6hr_2byte_%s_m%03d_%04d%02d.dr'%(self.vtype,scen, ens,Year,Mon)

        ny,nx,nvar = self.ny, self.nx, self.nvar
        nsteps     = os.stat( srcPath ).st_size / (ny*nx*nvar*2) # num of timesteps
        mmap   = np.memmap( srcPath, dtype='int16', mode='r'
                           ,shape=(nsteps, nvar, ny, nx))

        vidx   = self.vars.index(vname)
        a,b    = self.coefs[vidx]
        data   = ma.masked_equal(np.array( mmap[:, vidx, :, :] ).byteswap(), self.miss_in).mean(axis=0)*a + b
        return data





    def load_topo(self, vname='height'):
        return load_topo_TL319(baseDir=self.baseDir, vname=vname)


def load_topo_TL319(baseDir=None, vname='height'):
    ny,nx   = 320, 640
    miss    = -9.99e+33  
    vidx    = {'height':0, 'ratiol':1}[vname]
    srcPath = baseDir + '/fixed/TopogRatiol_gsmuv_TL319.gd'
    data    = ma.masked_equal(np.fromfile(srcPath, 'float32').byteswap().reshape(2,ny,nx)[vidx], miss)
    return data

def dLon():
    return 0.5625

def Lon():
    return np.arange(0,0.5625*639+0.001,0.5625)

def Lat():
    a1lat = np.array([
      -89.570,  -89.013,  -88.453,  -87.892,  -87.331,
      -86.769,  -86.208,  -85.647,  -85.085,  -84.523,
      -83.962,  -83.400,  -82.839,  -82.277,  -81.716,
      -81.154,  -80.592,  -80.031,  -79.469,  -78.908,
      -78.346,  -77.784,  -77.223,  -76.661,  -76.100,
      -75.538,  -74.976,  -74.415,  -73.853,  -73.291,
      -72.730,  -72.168,  -71.607,  -71.045,  -70.483,
      -69.922,  -69.360,  -68.799,  -68.237,  -67.675,
      -67.114,  -66.552,  -65.990,  -65.429,  -64.867,
      -64.306,  -63.744,  -63.182,  -62.621,  -62.059,
      -61.498,  -60.936,  -60.374,  -59.813,  -59.251,
      -58.689,  -58.128,  -57.566,  -57.005,  -56.443,
      -55.881,  -55.320,  -54.758,  -54.196,  -53.635,
      -53.073,  -52.512,  -51.950,  -51.388,  -50.827,
      -50.265,  -49.704,  -49.142,  -48.580,  -48.019,
      -47.457,  -46.895,  -46.334,  -45.772,  -45.211,
      -44.649,  -44.087,  -43.526,  -42.964,  -42.402,
      -41.841,  -41.279,  -40.718,  -40.156,  -39.594,
      -39.033,  -38.471,  -37.909,  -37.348,  -36.786,
      -36.225,  -35.663,  -35.101,  -34.540,  -33.978,
      -33.416,  -32.855,  -32.293,  -31.732,  -31.170,
      -30.608,  -30.047,  -29.485,  -28.924,  -28.362,
      -27.800,  -27.239,  -26.677,  -26.115,  -25.554,
      -24.992,  -24.431,  -23.869,  -23.307,  -22.746,
      -22.184,  -21.622,  -21.061,  -20.499,  -19.938,
      -19.376,  -18.814,  -18.253,  -17.691,  -17.129,
      -16.568,  -16.006,  -15.445,  -14.883,  -14.321,
      -13.760,  -13.198,  -12.636,  -12.075,  -11.513,
      -10.952,  -10.390,   -9.828,   -9.267,   -8.705,
       -8.144,   -7.582,   -7.020,   -6.459,   -5.897,
       -5.335,   -4.774,   -4.212,   -3.651,   -3.089,
       -2.527,   -1.966,   -1.404,   -0.842,   -0.281,
        0.281,    0.842,    1.404,    1.966,    2.527,
        3.089,    3.651,    4.212,    4.774,    5.335,
        5.897,    6.459,    7.020,    7.582,    8.144,
        8.705,    9.267,    9.828,   10.390,   10.952,
       11.513,   12.075,   12.636,   13.198,   13.760,
       14.321,   14.883,   15.445,   16.006,   16.568,
       17.129,   17.691,   18.253,   18.814,   19.376,
       19.938,   20.499,   21.061,   21.622,   22.184,
       22.746,   23.307,   23.869,   24.431,   24.992,
       25.554,   26.115,   26.677,   27.239,   27.800,
       28.362,   28.924,   29.485,   30.047,   30.608,
       31.170,   31.732,   32.293,   32.855,   33.416,
       33.978,   34.540,   35.101,   35.663,   36.225,
       36.786,   37.348,   37.909,   38.471,   39.033,
       39.594,   40.156,   40.718,   41.279,   41.841,
       42.402,   42.964,   43.526,   44.087,   44.649,
       45.211,   45.772,   46.334,   46.895,   47.457,
       48.019,   48.580,   49.142,   49.704,   50.265,
       50.827,   51.388,   51.950,   52.512,   53.073,
       53.635,   54.196,   54.758,   55.320,   55.881,
       56.443,   57.005,   57.566,   58.128,   58.689,
       59.251,   59.813,   60.374,   60.936,   61.498,
       62.059,   62.621,   63.182,   63.744,   64.306,
       64.867,   65.429,   65.990,   66.552,   67.114,
       67.675,   68.237,   68.799,   69.360,   69.922,
       70.483,   71.045,   71.607,   72.168,   72.730,
       73.291,   73.853,   74.415,   74.976,   75.538,
       76.100,   76.661,   77.223,   77.784,   78.346,
       78.908,   79.469,   80.031,   80.592,   81.154,
       81.716,   82.277,   82.839,   83.400,   83.962,
       84.523,   85.085,   85.647,   86.208,   86.769,
       87.331,   87.892,   88.453,   89.013,   89.570,],'float32')
    return a1lat


