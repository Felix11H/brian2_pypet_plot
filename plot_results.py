
import argparse, sys, os, itertools, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from matplotlib import rc

rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  

import numpy as np

from brian2.units import mV, ms, second

from pypet.trajectory import Trajectory
from pypet.brian2.parameter import Brian2Parameter, \
                                   Brian2MonitorResult



def load_trajectory(fname):
    
    tr = Trajectory(name='Example_23_BRIAN2', add_time=False,
                    filename=fname,
                    dynamic_imports=[Brian2MonitorResult,
                                     Brian2Parameter])

    # pypet.pypetconstants.LOAD_NOTHING  --> 0
    # pypet.pypetconstants.LOAD_SKELETON --> 1
    # pypet.pypetconstants.LOAD_DATA     --> 2
    tr.f_load(load_parameters=2, load_derived_parameters=2,
              load_results=1)
    tr.v_auto_load = True

    return tr



def analysis_figure(tr, crun):
    
    fig, (ax1,ax2) = pl.subplots(2,1)

    ax1.plot(tr.crun.StateMonitorV.t/ms,
             tr.crun.StateMonitorV.vm[0]/mV)
        
    ax2.plot(tr.crun.SpikeMonitor.t/ms, tr.crun.SpikeMonitor.i,
             marker='.', markersize=2, linestyle='None')
    

    ax1.set_xlabel('time [ms]')
    ax2.set_xlabel('time [ms]')

    ax1.set_ylabel('membrane voltage [mV]')
    ax2.set_ylabel('neuron index')

    ax1.set_title('$N={:d}$'.format(tr.N)+ \
                  r', $\tau=\text{\SI{'+ \
                  '{:.2f}'.format(tr.tauw/ms) + '}{ms}}$')

        
    directory = 'plots/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    fig.tight_layout()
        
    fig.savefig(directory+"/{:s}.png".format(crun),
                dpi=300, bbox_inches='tight')

    pl.close(fig)

    
if __name__ == "__main__":

    fname = sys.argv[1]
    
    tr = load_trajectory(fname)

    for crun in tr.f_iter_runs():
        analysis_figure(tr, crun)

