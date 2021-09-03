"""Plots and supply chain components for PTC and ITC proposed legislation"""

import numpy as np
import pandas as pd

if __name__ == '__main__':
    # Import CSVs with 30 GW pipeline
    DNV_gantt = 'U.S. OFfshore Wind Demand - Gantt Charts-20210730.xlsm'
    other_gantt = 'BAU_Floating_Gantt.xlsx'
    fixed_pipeline_30GW_raw = pd.read_excel(DNV_gantt, sheet_name='Aggregated', header=4, usecols='B:W', nrows=30)
    fixed_pipeline_BAU = pd.read_excel(other_gantt, sheet_name='BAU', header=0, usecols='A:O')
    float_pipeline = pd.read_excel(other_gantt, sheet_name='Floating', header=0, usecols='A:O')
    fixed_pipeline_30GW = pd.pivot_table(fixed_pipeline_30GW_raw, index='Project COD', aggfunc=np.sum).transpose().drop(['PROJECTS', 'UNDEVELOPPED AREAS'], axis=1)

