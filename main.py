"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = 'DNV_pipelines.xlsm'
    # Define scenarios to plot
    scenarios = ['EC-UNCONSTR', 'WC-UNC', 'EC-HIGH', 'GBF-UNC']
    # Define date range
    CODstart = 2022
    CODend = 2035
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

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='Figs/baseline_installedMW', y1max=10000, y2max=40000)

    # Significant supply chain constraints
    yvals_constr = [pipeline['EC-HIGH']['installMW'], pipeline['WC-UNC']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr, colors, names), fname='Figs/constrained_installedMW', y1max=10000, y2max=40000)

    # Constant throughput after 2029
    # Extend out baseline scenarios
    max_ind_fixed = 7  # 2028 - max fixed deployment
    max_ind_float = 8  # 2029 - max floating deployment
    num_repeat_fixed = len(COD_years) - max_ind_fixed
    num_repeat_float = len(COD_years) - max_ind_float

    expand_install_fixed = np.concatenate([pipeline['EC-UNCONSTR']['installMW'][0:max_ind_fixed],
                                           np.repeat(pipeline['EC-UNCONSTR']['installMW'][max_ind_fixed-1], num_repeat_fixed)])
    expand_install_float = np.concatenate([pipeline['WC-UNC']['installMW'][0:max_ind_float],
                                           np.repeat(pipeline['WC-UNC']['installMW'][max_ind_float-1], num_repeat_float)])

    yvals_expand = [expand_install_fixed, expand_install_float]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_expand, colors, names), fname='Figs/expanded_installedMW', y1max=10000)

    ### Number of projects and installation vessels
    yvals_proj = [pipeline['EC-UNCONSTR']['projects'], pipeline['WC-UNC']['projects']]
    y_vals_wtiv = pipeline['EC-UNCONSTR']['wtiv'] + pipeline['WC-UNC']['wtiv']
    y_vals_barge= pipeline['EC-UNCONSTR']['barge'] + pipeline['WC-UNC']['barge']
    y_vals_clv = pipeline['EC-UNCONSTR']['clv'] + pipeline['WC-UNC']['clv']
    y_vals_ctv = pipeline['EC-UNCONSTR']['ctv'] + pipeline['WC-UNC']['ctv']

    y_vessels = [y_vals_wtiv, y_vals_barge, y_vals_clv, y_vals_ctv]
    vessel_colors = ['#F7A11A','#5D9732','#933C06','#5E6A71']
    vessel_names = ['WTIV', 'Feeder barge', 'CLV', 'CTV']

    pr.stacked_bar_line(COD_years, zip(yvals_proj, colors, names), zip(y_vessels, vessel_colors, vessel_names),
                        fname='Figs/baseline_proj_vessels')

    #### Add for other scenarios

    ### Line plots for individual components
    y1 = pipeline['EC-UNCONSTR']
    y2 = pipeline['WC-UNC']
    component_plots = {
        'Turbines': {
                    'data': [y1['turb']+y2['turb'], y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': ['k','g','b','r'],
                    'names': ['Total', '12MW', '15MW','18MW'],
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': ['k', 'g', 'b', 'r'],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
        },
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/baseline_component_'+ k
        pr.line_plots(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name)


