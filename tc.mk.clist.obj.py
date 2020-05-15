from numpy import *
from collections import deque
from datetime import datetime, timedelta
from detect_fsub import *
import detect_func
import calendar
import util
#import config
import IO_Master
import ConstCyclone
import Cyclone
import os, sys
##--------------------------------------
#prj   = "JRA55"
#model = "__"
#run   = "__"
#res   = "145x288"
#plev_up  = 250
#noleap= False

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"
#plev_up  = 250
#noleap  = True

prj     = "d4PDF"
model   = "__"
#run     = "XX-HPB_NAT-100"   # {expr}-{scen}-{ens}
run     = "XX-HPB-001"   # {expr}-{scen}-{ens}
res     = "320x640"
plev_up  = 300
noleap  = False
dbbaseDir = '/home/utsumi/mnt/lab_work/hk01/d4PDF_GCM'
wsbaseDir = '/home/utsumi/mnt/lab_tank/utsumi/WS/d4PDF_GCM'


iDTime = datetime(2010,1,1,0)
eDTime = datetime(2010,1,5,0)

#iDTime = datetime(2006,1,1,6)
#eDTime = datetime(2015,1,1,0)

#-- argv ----------------
largv = sys.argv
if len(largv)>1:
  prj, model, run, res, noleap, dbbseDir, wsbaseDir = largv[1:1+7]
  if noleap=="True": noleap=True
  elif noleap=="False": noleap=False
  else: print "check noleap",noleap; sys.exit()

  iYear,iMon, eYear, eMon = map(int,largv[1+7:])
  eDay   = calendar.monthrange(eYear,eMon)[1]
  iDTime = datetime(iYear,iMon,1,0)   # 2020/04/28
  eDTime = datetime(eYear,eMon,eDay,18)
#-------------------------

dDTime = timedelta(hours=6)
ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)
lDTimeRev= lDTime[::-1]

#cfg          = config.cfg
#cfg['prj']   = prj    # for ConstCyclone
#cfg['model'] = model  # for ConstCyclone
#cfg['outbaseDir'] = cfg['baseDir'] + '/%s'%(run)
#iom    = IO_Master.IO_Master(cfg, prj, model, run, res)
iom    = IO_Master.IO_Master(prj, model, run, res, dbbaseDir)

const  = ConstCyclone.Const(prj=prj, model=model)
const['Lat'] = iom.Lat
const['Lon'] = iom.Lon
wsDir = wsbaseDir + '/%s'%(run)
cy     = Cyclone.Cyclone(baseDir=wsDir, const=const)

#singleday = True
singleday = False
unitdist  = 10.0 # km / hour
#unitdist  = 150.0 # km / hour  # test
#----------------
miss  = -9999.
#lvar  = ["rvort", "dtlow", "dtmid", "dtup", "wmeanlow", "wmeanup", "sst","land"]
lvar  = ["dtlow", "dtmid", "dtup", "wmeanlow", "wmeanup", "sst","land"]


a1lat = cy.Lat
a1lon = cy.Lon

def save_clist(var, a1dat, Year, Mon):
  clistDir, clistPath = cy.path_clist(var, Year, Mon)
  detect_func.mk_dir(clistDir)
  dNumType            = cy.dNumType

  array(a1dat, dtype=dNumType[var]).tofile(clistPath)  
  print clistPath

def ret_a2pgrad(DTime):
  return cy.load_a2dat("pgrad", DTime) 

#----------------------------
for idt, DTime in enumerate(lDTime):
  if ((idt==0)or(DTime.month != lDTime[idt-1].month)):
    Year = DTime.year
    Mon  = DTime.month
    #*** init ***********
    da1 = {}
    for var in lvar:
      da1[var]  = deque([])
    #********************
    # SST
    #-------------------- 
    a2sst = iom.Load_monSfc("sst", Year, Mon)  # t2m is called for d4PDF

    #********************
    # Land
    #-------------------- 
    a2land= iom.Load_const("land")
  #-------------------- 
  a2pgrad = cy.load_a2dat("pgrad",DTime)
  a2tlow  = iom.Load_6hrPlev("ta",DTime,850)
  a2tmid  = iom.Load_6hrPlev("ta",DTime,500)
  a2tup   = iom.Load_6hrPlev("ta",DTime,plev_up)
  a2ulow  = iom.Load_6hrPlev("ua",DTime,850)
  a2uup   = iom.Load_6hrPlev("ua",DTime,plev_up)
  a2vlow  = iom.Load_6hrPlev("va",DTime,850)
  a2vup   = iom.Load_6hrPlev("va",DTime,plev_up)
  
  tout = detect_fsub.calc_tcvar\
        (  a2pgrad.T, a2tlow.T, a2tmid.T, a2tup.T\
         , a2ulow.T, a2uup.T, a2vlow.T, a2vup.T\
         , a1lon, a1lat\
         , miss\
        )

  a2dtlow    = tout[0].T 
  a2dtmid    = tout[1].T 
  a2dtup     = tout[2].T 
  a2wmeanlow = tout[3].T 
  a2wmeanup  = tout[4].T 

  #---- shrink ---------------------
  #a1rvort_tmp     = ma.masked_where( a2pgrad==miss, a2rvort    ).compressed()
  a1dtlow_tmp     = ma.masked_where( a2pgrad==miss, a2dtlow    ).compressed()
  a1dtmid_tmp     = ma.masked_where( a2pgrad==miss, a2dtmid    ).compressed()
  a1dtup_tmp      = ma.masked_where( a2pgrad==miss, a2dtup     ).compressed()
  a1wmeanlow_tmp  = ma.masked_where( a2pgrad==miss, a2wmeanlow ).compressed()
  a1wmeanup_tmp   = ma.masked_where( a2pgrad==miss, a2wmeanup  ).compressed()
  a1sst_tmp       = ma.masked_where( a2pgrad==miss, a2sst      ).compressed()
  a1land_tmp      = ma.masked_where( a2pgrad==miss, a2land     ).compressed()

  #da1["rvort"   ].extend( a1rvort_tmp   )
  da1["dtlow"   ].extend( a1dtlow_tmp   )
  da1["dtmid"   ].extend( a1dtmid_tmp   )
  da1["dtup"    ].extend( a1dtup_tmp    )
  da1["wmeanlow"].extend( a1wmeanlow_tmp)
  da1["wmeanup" ].extend( a1wmeanup_tmp )
  da1["sst"     ].extend( a1sst_tmp     )
  da1["land"    ].extend( a1land_tmp    )
  #- write clist --
  if ((DTime==lDTime[-1])or(DTime.month != lDTime[idt+1].month)):
    for var in lvar:
      save_clist(var, da1[var], Year, Mon)
