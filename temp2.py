# %%
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import IO_d4PDF
from datetime import datetime
import config
%matplotlib inline

cfg   = config.cfg
vname = 'slp'
plev  = 850
dtime = datetime(2010,1,1,6)
run   = 'XX-HPB_NAT-100'
d4 = IO_d4PDF.IO_d4pdf(cfg, run)
a2dat= d4.Load_6hrSfc(vname, dtime)

plt.imshow(a2dat, origin='lower')
plt.colorbar()
plt.title(vname)
plt.show()

# %%
