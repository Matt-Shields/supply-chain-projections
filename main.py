"""Plots and supply chain components for PTC and ITC proposed legislation"""

import numpy as np
import pandas as pd
import plot_routines as pr

if __name__ == '__main__':
    # Import CSVs with 30 GW pipeline
    DNV_gantt = 'U.S. OFfshore Wind Demand - Gantt Charts-20210730.xlsm'
    other_gantt = 'BAU_Floating_Gantt.xlsx'
    fixed_pipeline_30GW_raw = pd.read_excel(DNV_gantt, sheet_name='Aggregated', header=4, usecols='B:W', nrows=30)
    fixed_pipeline_BAU = pd.read_excel(other_gantt, sheet_name='BAU', header=0, usecols='A:O',index_col='Project COD',)
    float_pipeline = pd.read_excel(other_gantt, sheet_name='Floating', header=0, usecols='A:O',index_col='Project COD',)
    fixed_pipeline_30GW = pd.pivot_table(fixed_pipeline_30GW_raw, index='Project COD', aggfunc=np.sum).transpose().drop(['PROJECTS', 'UNDEVELOPPED AREAS'], axis=1)

    # Stacked bar charts of fixed and floating with cumulative
    COD_years = fixed_pipeline_30GW.columns.to_numpy()
    # fixed_list = [fixed_pipeline_30GW.loc['Total Project Capacity, MW'], 'b', 'Fixed bottom (30 GW target)']
    # float_list = [float_pipeline.loc['Total Project Capacity, MW'], 'y', 'Floating (30 GW target)']

    # Single scenario
    yvals = [fixed_pipeline_30GW.loc['Total Project Capacity, MW'].to_numpy(), float_pipeline.loc['Total Project Capacity, MW'].to_numpy()]
    colors = ['b', 'y']
    names = ['Fixed bottom (30 GW target)', 'Floating (30 GW target)']


    # pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), '30GW_deployment')

    # Add BAU scenario
    yvals_BAU = [fixed_pipeline_BAU.loc['Total Project Capacity, MW'].to_numpy()]
    colors_BAU = ['g']
    names_BAU = ['Fixed-bottom (BAU)']

    fig, ax = pr.initFigAxis()

    pr.bar_cumulative_comp(COD_years, zip(yvals, colors, names), zip(yvals_BAU, colors_BAU,names_BAU), '30GW_BAU_deployment',
                           fig=fig, ax=ax, width = 0.35)












