"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars#, DNV_indices
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = 'DNV_pipelines.xlsm'
    # Define scenarios to plot
    scenarios = ['EC-UNCONSTR', 'WC-UNC']
    # Define date range
    CODstart = 2022
    CODend = 2030
    COD_years = np.arange(CODstart, CODend+1)
    # Loop through scenarios
    pipeline = {}
    for s in scenarios:
        # Read in Excel
        pipeline[s] = read_vars(file=DNV_gantt, sheet=s, xrange=COD_years)

    ######### GENERATE PLOTS
    ### Annual deployment + cumulative line
    # Baseline
    yvals = [pipeline['EC-UNCONSTR']['installMW'], pipeline['WC-UNC']['installMW']]
    colors = ['#0B5E90', '#00A4E4']
    names = ['Fixed bottom', 'Floating']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='Figs/baseline_installedMW', y1max=10000)



    # Create output data tables
    # fixed_30_group = fixed_pipeline_30GW.groupby(group_rows).sum().drop('Delete')
