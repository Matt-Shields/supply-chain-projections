"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars#, DNV_indices
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = '4.3 NREL Supply Chain Study-for NREL.v2.xlsm'
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


    # # Import CSVs with 30 GW pipeline
    #     # DNV_gantt = '4.3 NREL Supply Chain Study-for NREL.v2.xlsm'
    #     # DNV_gantt_v2 = '4.3 NREL Supply Chain Study-for NREL.v3.xlsx'
    #     # #other_gantt = 'All Scenarios_Varied LC_Jobs.xlsx'#'BAU_Floating_Gantt.xlsx'
    #     # fixed_pipeline_30GW_raw = pd.read_excel(DNV_gantt_v2, sheet_name='Aggregated', header=4, usecols='B:W', nrows=30,) #should header = none?
    #     # #fixed_pipeline_BAU = pd.read_excel(DNV_gantt, sheet_name='Aggregated', dtype=object, header=4, usecols='BD:BR',index_col='WC-UNDEVELOPED',)
    #     # float_pipeline_raw = pd.read_excel(DNV_gantt_v2, sheet_name='Aggregated', header=36, usecols='B:W',nrows=16,)
    #     # #float_pipeline = pd.read_excel(DNV_gantt, sheet_name='Aggregated', header=4, usecols='BD:BR',index_col='WC-UNDEVELOPED',)
    #     # fixed_pipeline_30GW = pd.pivot_table(fixed_pipeline_30GW_raw, index='Project COD', aggfunc=np.sum).transpose().drop(['PROJECTS', 'EC -UNDEVELOPED'], axis=1)
    #     # float_pipeline = pd.pivot_table(float_pipeline_raw, index='Project COD', aggfunc=np.sum).transpose().drop(['WC -UNDEVELOPED'], axis=1)
    #     #
    #     # #print(fixed_pipeline_30GW)
    #     # #print(float_pipeline)
    #     # # Stacked bar charts of fixed and floating with cumulative
    #     # COD_years = fixed_pipeline_30GW.columns.to_numpy()
    #     # #print(COD_years)
    #     # # Set max year if desired
    #     # xmax = 2030
    #     # try:
    #     #     # Set max COD on x axis
    #     #     COD_years = np.extract(COD_years < (xmax+1), COD_years)
    #     #     fixed_pipeline_30GW = fixed_pipeline_30GW[list(np.extract(COD_years < (xmax+1), COD_years))]
    #     #     #fixed_pipeline_BAU = fixed_pipeline_BAU[list(np.extract(COD_years < (xmax+1), COD_years))]
    #     #     float_pipeline = float_pipeline[list(np.extract(COD_years < (xmax+1), COD_years))]
    #     # except NameError:
    #     #     # xmax not defined
    #     #     pass


    # Total capacity
    # Single scenario
    yvals = [fixed_pipeline_30GW.loc['Total Project Capacity, MW'].to_numpy(), float_pipeline.loc['Total Project Capacity, MW'].to_numpy()]
    colors = ['#0B5E90', '#00A4E4']
    names = ['Fixed bottom (30 GW target)', 'Floating (30 GW target)']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='30GW_deployment', y1max=10000)

    #Figure 3 econ gaps assessment
    yvals_fig3 = [fixed_pipeline_30GW.loc['Total # of 12 MW turbines'].to_numpy(),
                  fixed_pipeline_30GW.loc['Total # of 15 MW turbines'].to_numpy(),
                    fixed_pipeline_30GW.loc['Total # of 18 MW turbines'].to_numpy()
                    ]
    colors_fig3 = ['#3D6321']
    names_fig3 = ['Fixed-bottom (low constrained)']

    #pr.bar_cumulative_comp(COD_years, zip(yvals, colors, names), zip(yvals_BAU, colors_BAU,names_BAU), fname='30GW_BAU_deployment',
                           #width = 0.35)


    # Add BAU scenario
    #yvals_BAU = [fixed_pipeline_BAU.loc['Total Project Capacity, MW'].to_numpy()]
    #colors_BAU = ['#3D6321']
    #names_BAU = ['Fixed-bottom (conservative)']

    #pr.bar_cumulative_comp(COD_years, zip(yvals, colors, names), zip(yvals_BAU, colors_BAU,names_BAU), fname='30GW_BAU_deployment',
                           #width = 0.35)

    # Vessels
    # y_vessels = pd.read_excel(DNV_gantt, sheet_name='OUTPUT-UNC', header=122, usecols='D:L', nrows=1).fillna(0).to_numpy()
    # pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), y_cum=y_vessels, fname='Vessels')

    # Create output data tables
    fixed_30_group = fixed_pipeline_30GW.groupby(group_rows).sum().drop('Delete')
