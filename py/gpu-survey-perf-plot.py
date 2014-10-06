#=========================================================================
# morph-trend-plot.py
#=========================================================================

import matplotlib.pyplot as plt
import math
import sys
import os.path
import numpy as np

#-------------------------------------------------------------------------
# Calculate figure size
#-------------------------------------------------------------------------
# We determine the fig_width_pt by using \showthe\columnwidth in LaTeX
# and copying the result into the script. Change the aspect ratio as
# necessary.

fig_width_pt  = 244.0
inches_per_pt = 1.0/72.27                     # convert pt to inch

aspect_ratio  = 0.6

fig_width     = 6.0                           # width in inches
fig_height    = fig_width * aspect_ratio      # height in inches
fig_size      = [ fig_width, fig_height ]

#-------------------------------------------------------------------------
# Configure matplotlib
#-------------------------------------------------------------------------

plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['font.size']          = 14
plt.rcParams['font.family']        = 'serif'
plt.rcParams['font.serif']         = ['Times']
plt.rcParams['figure.figsize']     = fig_size

#-------------------------------------------------------------------------
# Get data
#-------------------------------------------------------------------------

# Benchmarks

bmarks = [
  'BFS',  # USA-road-d.FLA.gr
  'BH',   # 1000000 1 0
  'DMR',  # r5M 12
  'MST',  # USA-road-d.FLA.gr
  'SP',   # 0 42000 10000 3
  'SSSP', # USA-road-d.FLA.gr
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'topology-driven',
  'data-driven',
]

num_configs = len( configs )

# Results (execution time in ms)

max_time = 1.0e12

time_data = [

  # topology-driven

  [
    1.0, 1.2, 1.0, 2.2, 1.0, 1.0
  ],

  # data-driven

  [
    4.9, 1.4, 2.8, 0.1, 2.2, 1.2
  ],

]

base_data = []

for tval, dval in zip( time_data[0], time_data[1] ):
  base_data.append( float( min( tval, dval ) ) )

perf_data = [ np.array( data ) / np.array( base_data ) for data in time_data ]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_bmarks )
mid = ( num_configs + 1 ) / 2.0

# Bar widths

width = 0.2

# Colors

colors = [
  '#cc6666',
  '#339999',
  '#339999',
  '#339999',
  '#339999',
]

# Patterns

patterns = [
  'x', '*', 'x', '*', 'o', '.',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Plot formatting

ax.set_xticks( ind+mid*width+width )
ax.set_xticklabels( bmarks )

ax.set_xlabel( 'Benchmarks', fontsize=18 )
ax.set_ylabel( 'Speedup',    fontsize=18 )

ax.grid( True )

# Set axis limits

plt.axis( xmax=num_bmarks-0.2, ymax=5.0 )

# Add bars for each configuration

rects = []

for i, perf in enumerate( perf_data ):
  rects.append( ax.bar( ind+width*i+width, perf, width, color=colors[i] ) )

# Add horizontal line for baseline

plt.axhline( y=1, color='k', linewidth=1.5 )

# Legend

ax.legend( rects, configs, loc='best', prop={'size':12} )

# Pretty layout

ax.xaxis.grid(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.tight_layout()

#-------------------------------------------------------------------------
# Generate PDF
#-------------------------------------------------------------------------

input_basename = os.path.splitext( os.path.basename(sys.argv[0]) )[0]
output_filename = input_basename + '.py.pdf'
plt.savefig( output_filename, bbox_inches='tight' )

