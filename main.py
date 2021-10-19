"""Plots and supply chain components for PTC and ITC proposed legislation"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows
import matplotlib.pyplot as plt

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

    # Set max year if desired
    xmax = 2030
    try:
        # Set max COD on x axis
        COD_years = np.extract(COD_years < (xmax+1), COD_years)
        fixed_pipeline_30GW = fixed_pipeline_30GW[list(np.extract(COD_years < (xmax+1), COD_years))]
        fixed_pipeline_BAU = fixed_pipeline_BAU[list(np.extract(COD_years < (xmax+1), COD_years))]
        float_pipeline = float_pipeline[list(np.extract(COD_years < (xmax+1), COD_years))]
    except NameError:
        # xmax not defined
        pass
    # Total capacity
    # Single scenario
    yvals = [fixed_pipeline_30GW.loc['Total Project Capacity, MW'].to_numpy(), float_pipeline.loc['Total Project Capacity, MW'].to_numpy()]
    colors = ['#0B5E90', '#00A4E4']
    names = ['Fixed bottom (30 GW target)', 'Floating (30 GW target)']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='30GW_deployment', y1max=10000)

    # Add BAU scenario
    yvals_BAU = [fixed_pipeline_BAU.loc['Total Project Capacity, MW'].to_numpy()]
    colors_BAU = ['#3D6321']
    names_BAU = ['Fixed-bottom (conservative)']

    pr.bar_cumulative_comp(COD_years, zip(yvals, colors, names), zip(yvals_BAU, colors_BAU,names_BAU), fname='30GW_BAU_deployment',
                           width = 0.35)

    # Vessels
    # y_vessels = pd.read_excel(DNV_gantt, sheet_name='OUTPUT-UNC', header=122, usecols='D:L', nrows=1).fillna(0).to_numpy()
    # pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), y_cum=y_vessels, fname='Vessels')

    # Create output data tables
    fixed_30_group = fixed_pipeline_30GW.groupby(group_rows).sum().drop('Delete')












