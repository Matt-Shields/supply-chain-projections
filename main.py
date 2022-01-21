"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars, read_component_jobvars, read_varsTot, read_jobvars_WC, \
    colors_list, read_varsEC, read_varsGDP, read_varsTot_constrained
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = 'US OSW EC-WC Pipeline Gantt Charts 20220119.xlsm'
    # Define scenarios to plot
    scenarios = ['EC-known', 'WC-known', 'EC-HIGH', 'EC-LOW', 'GBF-UNC', 'ALL-MONO', 'FIX-EX','FLOAT-EX']
    # Define date range
    CODstart = 2022
    CODend = 2035
    COD_years = np.arange(CODstart, CODend+1)
    # Loop through scenarios
    pipeline = {}
    for s in scenarios:
        # Read in Excel
        if 'WC' in s:
            pipeline[s] = read_vars(file=DNV_gantt, sheet=s, xrange=COD_years)
        else:
            pipeline[s] = read_vars(file=DNV_gantt, sheet=s, xrange=COD_years)

    ######### GENERATE PLOTS
    ### Annual deployment + cumulative line
    y1max_deploy = 10000
    y2max_deploy = 60000
    y1max_turbines = 450
    y2max_turbines = 3500
    y1max_foundations = 450
    y2max_foundations = 3500
    y1max_cables = 2500
    y2max_cables = 20000
    y1max_vessels = 140

    # Baseline
    yvals = [pipeline['EC-known']['installMW'], pipeline['WC-known']['installMW']]
    colors = [colors_list['fixed'], colors_list['float']]
    names = ['Fixed bottom', 'Floating']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='Figs/baseline_installedMW',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    # Significant supply chain constraints
    yvals_constr = [pipeline['EC-HIGH']['installMW'], pipeline['WC-known']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr, colors, names), fname='Figs/constrained_installedMW_high',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    # Moderate supply chain constraints
    yvals_constr_low = [pipeline['EC-LOW']['installMW'], pipeline['WC-known']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr_low, colors, names), fname='Figs/constrained_installedMW_low',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    # Expanded leasing baseline
    # Extend out baseline scenarios
    # max_ind_fixed = 7  # 2028 - max fixed deployment
    # max_ind_float = 8  # 2029 - max floating deployment
    # num_repeat_fixed = len(COD_years) - max_ind_fixed
    # num_repeat_float = len(COD_years) - max_ind_float
    #
    # expand_install_fixed = {}
    # expand_install_float = {}
    # for k,v in pipeline['EC-known'].items():
    #     expand_install_fixed[k] = np.concatenate(
    #         [v[0:max_ind_fixed], np.repeat(v[max_ind_fixed-1], num_repeat_fixed)])
    # for k, v in pipeline['WC-known'].items():
    #     expand_install_float[k] = np.concatenate(
    #         [v[0:max_ind_float], np.repeat(v[max_ind_float - 1], num_repeat_float)])
    # yvals_expand = [expand_install_fixed['installMW'], expand_install_float['installMW']]
    #
    # pr.stacked_bar_cumulative(COD_years, zip(yvals_expand, colors, names), fname='Figs/expanded_installedMW',
    #                           y1max=y1max_deploy, y2max=y2max_deploy)

    # Updated expanded leasing scenarios
    yvals_exp2 = [pipeline['EC-known']['installMW'], pipeline['WC-known']['installMW'], pipeline['FIX-EX']['installMW'], pipeline['FLOAT-EX']['installMW']]
    colors_exp2 = [colors_list['fixed'], colors_list['float'],colors_list['expand_fix'], colors_list['expand_float']]
    names_exp2 = ['Fixed bottom', 'Floating', 'Anticipated fixed bottom leasing', 'Anticipated floating leasing']

    pr.stacked_bar_cumulative(COD_years, zip(yvals_exp2, colors_exp2, names_exp2), fname='Figs/expanded2_installedMW',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    ### Number of projects and installation vessels
    # yvals_proj = [pipeline['EC-known']['projects'], pipeline['WC-known']['projects']]
    # y_vals_wtiv = pipeline['EC-known']['wtiv']
    # y_vals_barge= pipeline['EC-known']['barge']
    # y_vals_clv = pipeline['EC-known']['clv'] + pipeline['WC-known']['clv']
    # y_vals_ctv = pipeline['EC-known']['ctv'] + pipeline['WC-known']['ctv']
    #
    # y_vessels = [y_vals_wtiv, y_vals_barge, y_vals_clv, y_vals_ctv]
    # vessel_colors = [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv']]
    # vessel_names = ['WTIV', 'Feeder barge', 'CLV', 'CTV']
    #
    # pr.stacked_bar_line(COD_years, zip(yvals_proj, colors, names), zip(y_vessels, vessel_colors, vessel_names),
    #                     fname='Figs/baseline_proj_vessels', myylabel='Installed projects', myy2label='Number of vessels')

    #### Add for other scenarios

    ### Line plots for individual components
    # Baseline
    y1 = pipeline['EC-known']
    y2 = pipeline['WC-known']
    y3 = pipeline['FIX-EX']
    y4 = pipeline['FLOAT-EX']

    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW']+y3['turb12MW']+y4['turb12MW'],
                             y1['turb15MW']+y2['turb15MW']+y3['turb15MW']+y4['turb15MW'],
                             y1['turb18MW']+y2['turb18MW']+y3['turb18MW']+y4['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines',
                    'y2label': 'number of turbines',
                    'y1max': y1max_turbines,
                    'y2max': y2max_turbines
                    },
        'Foundations': {
            'data': [y1['monopiles']+y3['monopiles'], y1['jacket']+y3['jacket'], y1['gbf']+y3['gbf'], y2['semi']+y4['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations',
            'y2label': 'number of foundations',
            'y1max': y1max_foundations,
            'y2max': y2max_foundations
        },
        'Cables': {
            'data': [y1['array']+y3['array'], y1['export']+y3['export'], y2['array']+y4['array'], y2['export']+y4['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km',
            'y2label': 'length of cable, km',
            'y1max': y1max_cables,
            'y2max': y2max_cables
        },
        'Vessels':{
            'data': [y1['wtiv']+y3['wtiv'], y1['barge']+y1['barge'], y1['clv']+y2['clv']+y3['clv']+y4['clv'],
                     y1['sov']+y2['sov']+y3['sov']+y4['sov'], y1['ctv']+y2['ctv']+y3['ctv']+y4['ctv'],
                          y2['tugs']+y4['tugs'], y2['ahts']+y4['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['sov'],
                       colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'SOV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of vessels',
            'y1max': y1max_vessels,
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/baseline_component_' + k
        if 'Vessel' in k:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'],
                                      cumulative_line=False, y1max=v['y1max'])
        else:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'], myy2label='Cumulative ' + v['y2label'],
                                      y1max=v['y1max'], y2max=v['y2max'])

    ###Baseline vessels
    #y1 = pipeline['EC-known']
    #y2 = pipeline['WC-known']


    # Significant supply chain constraints
    y1 = pipeline['EC-HIGH']
    y2 = pipeline['WC-known']
    # Todo: Add expanded
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines',
                    'y2label': 'number of turbines',
                    'y1max': y1max_turbines,
                    'y2max': y2max_turbines
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations',
            'y2label': 'number of foundations',
            'y1max': y1max_foundations,
            'y2max': y2max_foundations
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km',
            'y2label': 'length of cable, km',
            'y1max': y1max_cables,
            'y2max': y2max_cables
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['sov']+y2['sov'],y1['ctv']+y2['ctv'],
                          y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['sov'],
                       colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'SOV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of vessels',
            'y1max': y1max_vessels,
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/constrained_high_component_'+ k
        if 'Vessel' in k:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'],
                                      cumulative_line=False, y1max=v['y1max'])
        else:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'], myy2label='Cumulative ' + v['y2label'],
                                      y1max=v['y1max'], y2max=v['y2max'])

    # Moderate supply chain constraints
    y1 = pipeline['EC-LOW']
    y2 = pipeline['WC-known']
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines',
                    'y2label': 'number of turbines',
                    'y1max': y1max_turbines,
                    'y2max': y2max_turbines
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations',
            'y2label': 'number of foundations',
            'y1max': y1max_foundations,
            'y2max': y2max_foundations
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km',
            'y2label': 'length of cable, km',
            'y1max': y1max_cables,
            'y2max': y2max_cables
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['sov']+y2['sov'],y1['ctv']+y2['ctv'],
                          y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['sov'],
                       colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'SOV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of vessels',
            'y1max': y1max_vessels,
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/constrained_low_component_'+ k
        if 'Vessel' in k:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'],
                                      cumulative_line=False, y1max=v['y1max'])
        else:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'], myy2label='Cumulative ' + v['y2label'],
                                      y1max=v['y1max'], y2max=v['y2max'])

    # Expanded pipeline
    # y1 = expand_install_fixed
    # y2 = expand_install_float
    # component_plots = {
    #     'Turbines': {
    #         'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
    #         'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
    #         'names': [ '12MW', '15MW','18MW'],
    #         'ylabel': 'Number of turbines',
    #         'y1max': y1max_turbines,
    #         'y2max': y2max_turbines
    #         },
    #     'Foundations': {
    #         'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
    #         'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
    #         'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
    #         'ylabel': 'Number of foundations',
    #         'y1max': y1max_foundations,
    #         'y2max': y2max_foundations
    #     },
    #     'Cables': {
    #         'data': [y1['array'], y1['export'], y2['array'], y2['export']],
    #         'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
    #         'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
    #         'ylabel': 'Length of cable, km',
    #         'y1max': y1max_cables,
    #         'y2max': y2max_cables
    #     },
    #     'Vessels':{
    #         'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
    #         'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
    #         'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
    #         'ylabel': 'Number of vessels',
    #         'y1max': y1max_vessels
    #     }
    # }
    #
    # for k, v in component_plots.items():
    #     plot_name = 'Figs/expanded_component_'+ k
    #     if 'Vessel' in k:
    #         pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
    #                                   myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'],
    #                                   cumulative_line=False, y1max=v['y1max'])
    #     else:
    #         pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
    #                                   myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'],
    #                                   y1max=v['y1max'], y2max=v['y2max'])

    # GBF market share
    y1 = pipeline['GBF-UNC']
    y2 = pipeline['WC-known']
    component_plots = {
        'Turbines': {
            'data': [y1['turb12MW'] + y2['turb12MW'], y1['turb15MW'] + y2['turb15MW'], y1['turb18MW'] + y2['turb18MW']],
            'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
            'names': ['12MW', '15MW', '18MW'],
            'ylabel': 'Number of turbines',
            'y1max': y1max_turbines,
            'y2max': y2max_turbines

        },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations',
            'y1max': y1max_foundations,
            'y2max': y2max_foundations
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'],
                       colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km',
            'y1max': y1max_cables,
            'y2max': y2max_cables
        },
        'Vessels': {
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['sov']+y2['sov'],y1['ctv']+y2['ctv'],
                          y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['sov'],
                       colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'SOV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of vessels',
            'y1max': y1max_vessels
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/uniform_found_component_'+ k
        if 'Vessel' in k:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'],
                                      cumulative_line=False, y1max=v['y1max'])
        else:
            pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                      myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'],
                                      y1max=v['y1max'], y2max=v['y2max'])

    ## Berths and laydown area
    # y_EC_berth = pipeline['EC-known']
    # y_WC_berth = pipeline['WC-known']

    yvals_berths = [pipeline['EC-known']['berths'] + pipeline['FIX-EX']['berths'],
                    pipeline['WC-known']['berths'] + pipeline['FLOAT-EX']['berths']
                    ]
    colors_berths = [colors_list['fixed'], colors_list['float']]
    names_berths = ['Fixed bottom', 'Floating']

    pr.stacked_bar_cumulative(COD_years, zip(yvals_berths, colors_berths, names_berths), fname='Figs/berths',
                              cumulative_line=False)

    #JEDI - Varied Scenarios graphs

    JEDI_pipeline = 'Total-Expand_Jobs and EC-UNC.xlsx' # Define input spreadsheet - total jobs + fixed bottom component jobs
    JEDI_floating_pipeline = 'WC-UNC.xlsx' # floating component jobs
    JEDI_constrained_pipeline = 'EC-UNC Constraints.xlsx' # Constrained East Coast deployment
    JEDI_GDP_induced = 'Total-Expand_GDP and Induced Impacts.xlsx' # GDP and induced jobs for baseline

    scenarios_JEDI = ['Total-Expand Scenario', 'Nacelle', 'Rotor Blades', 'Towers', 'Monopiles', 'Transition Piece',
                      'Jacket (For Turbine)', 'GBF', 'Jacket (For Substation)', 'Substation (Topside)', 'Array Cable',
                      'Export Cable'] #Define sheet to pull from to plot scenarios
    scenarios_JEDI_floating = ['WC Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Floating (semisubmersible)', 'Floating (floating OSS)',
                      'Floating OSS Topside', 'Array Cable', 'Export Cable'] #Define sheet to pull from to plot scenarios
    scenarios_JEDI_constrained = ['Constrained Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Monopiles', 'Transition Piece',
                      'Jacket (For Turbine)', 'GBF', 'Jacket (For Substation)', 'Substation (Topside)', 'Array Cable',
                      'Export Cable']  # Define sheet to pull from to plot scenarios
    GDP_ECWC = ['Total-Expand GDP', 'Total-Expand Induced Impacts']

    #data start and end dates
    dateStart = 2021
    dateEnd = 2033
    dateYrs = np.arange(dateStart, dateEnd+1)

    ### Total job demand, EC+ WC
    ECWCPipeline = {}
    ECWCPipeline['Total-Expand Scenario'] = read_varsTot(file=JEDI_pipeline,
                                                         sheet='Total-Expand Scenario',
                                                         xrange=dateYrs) #read in Excel
    colors_tot = ['k', 'k']
    names_tot = ['25% Domestic Content, Total Workforce Baseline Scenario',
                 '100% Domestic Content, Total Workforce Baseline Scenario']
    lines_tot = ['dashed', 'solid']

    # Baseline
    yvals_EC = [ECWCPipeline['Total-Expand Scenario']['25demandTot_UNC'],
                ECWCPipeline['Total-Expand Scenario']['100demandTot_UNC']]
    pr.line_plots2(dateYrs, zip(yvals_EC, colors_tot, lines_tot, names_tot), fname='Figs/Total_Workforce_Demand',
                   ymax=85000)

    ### Constrained throughput
    ECWCPipeline['Constrained'] = read_varsTot_constrained(file=JEDI_constrained_pipeline,
                                                            sheet='Constrained Scenarios',
                                                            xrange=dateYrs)
    # Moderate
    yvals_EC_mod = [ECWCPipeline['Constrained']['25demandTot_LOW'],
                    ECWCPipeline['Constrained']['100demandTot_LOW']]
    pr.line_plots2(dateYrs, zip(yvals_EC_mod, colors_tot, lines_tot, names_tot), fname='Figs/Total_Workforce_Demand_ModerateCstr',
                   ymax=85000)

    # Significant
    yvals_EC_sig = [ECWCPipeline['Constrained']['25demandTot_HIGH'],
                    ECWCPipeline['Constrained']['100demandTot_HIGH']]
    pr.line_plots2(dateYrs, zip(yvals_EC_sig, colors_tot, lines_tot, names_tot), fname='Figs/Total_Workforce_Demand_SigCstr',
                   ymax=85000)

    ### Area plots for component demand
    # EC_jobs_LH = {}
    jobsPipeline = {}
    jobsPipeline_lh = {}
    jobsPipeline_floating = {}
    totalGDP = {}
    for s in scenarios_JEDI:
        jobsPipeline[s] = read_component_jobvars(file=JEDI_pipeline, sheet=s, xrange=dateYrs) #read in Excel
        # EC_jobs_LH[s] = read_varsEC(file=JEDI_pipeline, sheet=s, xrange=dateYrs)
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')
    for s in scenarios_JEDI_floating:
        jobsPipeline_floating[s] = read_jobvars_WC(file=JEDI_floating_pipeline, sheet=s, xrange=dateYrs)  # read in Excel
    for s in scenarios_JEDI_constrained:
        jobsPipeline_lh[s] = read_varsEC(file=JEDI_constrained_pipeline, sheet=s, xrange=dateYrs)  # read in Excel
    for s in GDP_ECWC:
        totalGDP[s] = read_varsGDP(file=JEDI_GDP_induced, sheet=s, xrange=dateYrs)  # read in Excel

    # Component demand, East coast
    # p0 = EC_jobs_LH['Total-Expand Scenario']
    p1 = jobsPipeline['Nacelle']
    p2 = jobsPipeline['Rotor Blades']
    p3 = jobsPipeline['Towers']
    p4 = jobsPipeline['Monopiles']
    p5 = jobsPipeline['Transition Piece']
    p6 = jobsPipeline['Jacket (For Turbine)']
    p7 = jobsPipeline['GBF']
    p8 = jobsPipeline['Jacket (For Substation)']
    p9 = jobsPipeline['Substation (Topside)']
    p10 = jobsPipeline['Array Cable']
    p11 = jobsPipeline['Export Cable']

    p1_lh = jobsPipeline_lh['Nacelle']
    p2_lh = jobsPipeline_lh['Rotor Blades']
    p3_lh = jobsPipeline_lh['Towers']
    p4_lh = jobsPipeline_lh['Monopiles']
    p5_lh = jobsPipeline_lh['Transition Piece']
    p6_lh = jobsPipeline_lh['Jacket (For Turbine)']
    p7_lh = jobsPipeline_lh['GBF']
    p8_lh = jobsPipeline_lh['Jacket (For Substation)']
    p9_lh = jobsPipeline_lh['Substation (Topside)']
    p10_lh = jobsPipeline_lh['Array Cable']
    p11_lh = jobsPipeline_lh['Export Cable']


    # West Cast
    # p0 = EC_jobs_LH['WC Scenarios']
    p1_fl = jobsPipeline_floating['Nacelle']
    p2_fl = jobsPipeline_floating['Rotor Blades']
    p3_fl = jobsPipeline_floating['Towers']
    p4_fl = jobsPipeline_floating['Floating (semisubmersible)']
    p5_fl = jobsPipeline_floating['Floating (floating OSS)']
    p6_fl = jobsPipeline_floating['Floating OSS Topside']
    p7_fl = jobsPipeline_floating['Array Cable']
    p8_fl = jobsPipeline_floating['Export Cable']

    # scenario_plots_LH = {
    #     'Low_Scenario': {
    #     'data': [p0['25demandEC_LOW'], p0['100demandEC_LOW']],
    #     'colors': [colors_list['ctv'], colors_list['tugs']],
    #     'names': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints'],
    #     'lines': ['dashed','solid'],
    #     'yvalmax': 60000
    #     },
    #
    #     'High_Scenario': {
    #     'data': [p0['25demandEC_HIGH'], p0['100demandEC_HIGH']],
    #     'colors': [colors_list['ctv'], colors_list['tugs']],
    #     'names': ['25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
    #     'lines': ['dashed','solid'],
    #     'yvalmax': 60000
    #     }
    # }

    workforce_plots = {

        'JobPlots100': {
            'data':[p1['100domEC_UNC'], p2['100domEC_UNC'], p3['100domEC_UNC'], p4['100domEC_UNC'], p5['100domEC_UNC'], p6['100domEC_UNC'], p7['100domEC_UNC'], p8['100domEC_UNC'], p9['100domEC_UNC'], p10['100domEC_UNC'], p11['100domEC_UNC']],
            'colors': [colors_list['fixed'], colors_list['rotors'], colors_list['towers'], colors_list['monopiles'], colors_list['transp'], colors_list['jackt_t'], colors_list['gbfs'], colors_list['jackets'], colors_list['subt'], colors_list['static_array'], colors_list['static_export']],
            'names': ['Nacelle', 'Rotor blades', 'Towers', 'Monopiles', 'Transition piece', 'Jacket', 'GBF', 'Substation jacket', 'Substation topside', 'Array cable', 'Export cable']
            #'names_100': ['100% Domestic Content, Nacelle Baseline Scenario', '100% Domestic Content, Rotor Blades Baseline Scenario', '100% Domestic Content, Towers Baseline Scenario', '100% Domestic Content, Monopiles Baseline Scenario',
                #'100% Domestic Content, Transition Piece Baseline Scenario', '100% Domestic Content, Jacket (For Turbine) Baseline Scenario', '100% Domestic Content, GBF Baseline Scenario', '100% Domestic Content, Jacket (For Substation) Baseline Scenario',
                #'100% Domestic Content, Substation (Topside) Baseline Scenario', '100% Domestic Content, Array Cable Baseline Scenario', '100% Domestic Content, Export Cable Baseline Scenario']
        },
        'JobPlots25': {
            'data':[p1['25domEC_UNC'], p2['25domEC_UNC'], p3['25domEC_UNC'], p4['25domEC_UNC'], p5['25domEC_UNC'], p6['25domEC_UNC'], p7['25domEC_UNC'], p8['25domEC_UNC'], p9['25domEC_UNC'], p10['25domEC_UNC'], p11['25domEC_UNC']],
            'colors': [colors_list['fixed'], colors_list['rotors'], colors_list['towers'], colors_list['monopiles'], colors_list['transp'], colors_list['jackt_t'], colors_list['gbfs'], colors_list['jackets'], colors_list['subt'], colors_list['static_array'], colors_list['static_export']],
            'names': ['Nacelle', 'Rotor blades', 'Towers', 'Monopiles', 'Transition piece', 'Jacket', 'GBF', 'Substation jacket', 'Substation topside', 'Array cable', 'Export cable']
            #'names_25': ['25% Domestic Content, Nacelle Baseline Scenario', '25% Domestic Content, Rotor Blades Baseline Scenario', '25% Domestic Content, Towers Baseline Scenario', '25% Domestic Content, Monopiles Baseline Scenario',
                #'25% Domestic Content, Transition Piece Baseline Scenario', '25% Domestic Content, Jacket (For Turbine) Baseline Scenario', '25% Domestic Content, GBF Baseline Scenario', '25% Domestic Content, Jacket (For Substation) Baseline Scenario',
                #'25% Domestic Content, Substation (Topside) Baseline Scenario', '25% Domestic Content, Array Cable Baseline Scenario', '25% Domestic Content, Export Cable Baseline Scenario']
        }
    }

    workforce_plots_floating = {

        'JobPlots100': {
            'data': [p1_fl['100domWC_UNC'], p2_fl['100domWC_UNC'], p3_fl['100domWC_UNC'], p4_fl['100domWC_UNC'], p5_fl['100domWC_UNC'],
                     p6_fl['100domWC_UNC'], p7_fl['100domWC_UNC'], p8_fl['100domWC_UNC']],
            'colors': [colors_list['fixed'], colors_list['rotors'], colors_list['towers'], colors_list['monopiles'],
                       colors_list['transp'], colors_list['subt'], colors_list['static_array'], colors_list['dynamic_export']],
            'names': ['Nacelle', 'Rotor blades', 'Towers', 'Floating platform', 'Substation platform', 'Substation topside',
                      'Dynamic array cable', 'Dynamic export cable']
            # 'names_100': ['100% Domestic Content, Nacelle Baseline Scenario', '100% Domestic Content, Rotor Blades Baseline Scenario', '100% Domestic Content, Towers Baseline Scenario', '100% Domestic Content, Monopiles Baseline Scenario',
            # '100% Domestic Content, Transition Piece Baseline Scenario', '100% Domestic Content, Jacket (For Turbine) Baseline Scenario', '100% Domestic Content, GBF Baseline Scenario', '100% Domestic Content, Jacket (For Substation) Baseline Scenario',
            # '100% Domestic Content, Substation (Topside) Baseline Scenario', '100% Domestic Content, Array Cable Baseline Scenario', '100% Domestic Content, Export Cable Baseline Scenario']
        },
        'JobPlots25': {
            'data': [p1_fl['25domWC_UNC'], p2_fl['25domWC_UNC'], p3_fl['25domWC_UNC'], p4_fl['25domWC_UNC'], p5_fl['25domWC_UNC'],
                     p6_fl['25domWC_UNC'], p7_fl['25domWC_UNC'], p8_fl['25domWC_UNC']],
            'colors': [colors_list['fixed'], colors_list['rotors'], colors_list['towers'], colors_list['monopiles'],
                       colors_list['transp'], colors_list['subt'], colors_list['static_array'], colors_list['dynamic_export']],
            'names': ['Nacelle', 'Rotor blades', 'Towers', 'Floating platform', 'Substation platform', 'Substation topside',
                      'Dynamic array cable', 'Dynamic export cable']
            # 'names_25': ['25% Domestic Content, Nacelle Baseline Scenario', '25% Domestic Content, Rotor Blades Baseline Scenario', '25% Domestic Content, Towers Baseline Scenario', '25% Domestic Content, Monopiles Baseline Scenario',
            # '25% Domestic Content, Transition Piece Baseline Scenario', '25% Domestic Content, Jacket (For Turbine) Baseline Scenario', '25% Domestic Content, GBF Baseline Scenario', '25% Domestic Content, Jacket (For Substation) Baseline Scenario',
            # '25% Domestic Content, Substation (Topside) Baseline Scenario', '25% Domestic Content, Array Cable Baseline Scenario', '25% Domestic Content, Export Cable Baseline Scenario']
        }
    }

    for k, v in workforce_plots.items():
        plot_name = 'Figs/Fixed_JobRequirements_' + k
        pr.area_plotsv2(dateYrs, zip(v['data'], v['colors'], v['names']), ymax = 70000, fname=plot_name)

    for k, v in workforce_plots_floating.items():
        plot_name = 'Figs/Floating_JobRequirements_' + k
        pr.area_plotsv2(dateYrs, zip(v['data'], v['colors'], v['names']), ymax = 50000, fname=plot_name)

    ### Fixed bottomn component demand plots
    scenario_plots = {

        'Nacelle': {
            'data': [p1['25domEC_UNC'], p1['100domEC_UNC']],
            'data_lh': [p1_lh['25demandEC_LOW'], p1_lh['100demandEC_LOW'], p1_lh['25demandEC_HIGH'], p1_lh['100demandEC_HIGH']],
            'data100':[p1['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_100': ['100% Domestic Content, Nacelle Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 35000,
            'yval_lh': 35000
        },
        'Rotor Blades': {
            'data': [p2['25domEC_UNC'], p2['100domEC_UNC']],
            'data_lh': [p2_lh['25demandEC_LOW'], p2_lh['100demandEC_LOW'], p2_lh['25demandEC_HIGH'], p2_lh['100demandEC_HIGH']],
            'data25':[p2['25domEC_UNC']],
            'data100':[p2['100domEC_UNC']],
            'colors_25_100': [colors_list['rotors']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Rotor Blades Baseline Scenario'],
            'names_100': ['100% Domestic Content, Rotor Blades Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 6000,
            'yval_lh': 6000

        },
        'Towers': {
            'data': [p3['25domEC_UNC'], p3['100domEC_UNC']],
            'data_lh': [p3_lh['25demandEC_LOW'], p3_lh['100demandEC_LOW'], p3_lh['25demandEC_HIGH'], p3_lh['100demandEC_HIGH']],
            'data25':[p3['25domEC_UNC']],
            'data100':[p3['100domEC_UNC']],
            'colors_25_100': [colors_list['towers']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Tower Baseline Scenario'],
            'names_100': ['100% Domestic Content, Tower Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 8050,
            'yval_lh': 8050
        },
        'Monopiles': {
            'data': [p4['25domEC_UNC'], p4['100domEC_UNC']],
            'data_lh': [p4_lh['25demandEC_LOW'], p4_lh['100demandEC_LOW'], p4_lh['25demandEC_HIGH'], p4_lh['100demandEC_HIGH']],
            'data25':[p4['25domEC_UNC']],
            'data100':[p4['100domEC_UNC']],
            'colors_25_100': [colors_list['monopiles']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Monopile Baseline Scenario'],
            'names_100': ['100% Domestic Content, Monopile Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 9000,
            'yval_lh': 10000
        },
        'Transition Piece': {
            'data': [p5['25domEC_UNC'], p5['100domEC_UNC']],
            'data_lh': [p5_lh['25demandEC_LOW'], p5_lh['100demandEC_LOW'], p5_lh['25demandEC_HIGH'], p5_lh['100demandEC_HIGH']],
            'data25':[p5['25domEC_UNC']],
            'data100':[p5['100domEC_UNC']],
            'colors_25_100': [colors_list['transp']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Transition Piece Baseline Scenario'],
            'names_100': ['100% Domestic Content, Transition Piece Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 5000,
            'yval_lh': 5500
        },
        'Jacket (For Turbine)': {
            'data': [p6['25domEC_UNC'], p6['100domEC_UNC']],
            'data_lh': [p6_lh['25demandEC_LOW'], p6_lh['100demandEC_LOW'], p6_lh['25demandEC_HIGH'], p6_lh['100demandEC_HIGH']],
            'data25':[p6['25domEC_UNC']],
            'data100':[p6['100domEC_UNC']],
            'colors_25_100': [colors_list['jackt_t']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Jacket (For Turbine) Baseline Scenario'],
            'names_100': ['100% Domestic Content, Jacket (For Turbine) Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 5000,
            'yval_lh': 5250
        },
        'GBF': {
            'data': [p7['25domEC_UNC'], p7['100domEC_UNC']],
            'data_lh': [p7_lh['25demandEC_LOW'], p7_lh['100demandEC_LOW'], p7_lh['25demandEC_HIGH'], p7_lh['100demandEC_HIGH']],
            'data25':[p7['25domEC_UNC']],
            'data100':[p7['100domEC_UNC']],
            'colors_25_100': [colors_list['gbfs']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, GBF Baseline Scenario'],
            'names_100': ['100% Domestic Content, GBF Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 8900,
            'yval_lh': 8950
        },
        'Jacket (For Substation)': {
            'data': [p8['25domEC_UNC'], p8['100domEC_UNC']],
            'data_lh': [p8_lh['25demandEC_LOW'], p8_lh['100demandEC_LOW'], p8_lh['25demandEC_HIGH'], p8_lh['100demandEC_HIGH']],
            'data25':[p8['25domEC_UNC']],
            'data100':[p8['100domEC_UNC']],
            'colors_25_100': [colors_list['jackets']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Jacket (For Substation) Baseline Scenario'],
            'names_100': ['100% Domestic Content, Jacket (For Substation) Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 85,
            'yval_lh': 85
        },
        'Substation (Topside)': {
            'data': [p9['25domEC_UNC'], p9['100domEC_UNC']],
            'data_lh': [p9_lh['25demandEC_LOW'], p9_lh['100demandEC_LOW'], p9_lh['25demandEC_HIGH'], p9_lh['100demandEC_HIGH']],
            'data25':[p9['25domEC_UNC']],
            'data100':[p9['100domEC_UNC']],
            'colors_25_100': [colors_list['subt']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            'names_25': ['25% Domestic Content, Substation (Topside) Baseline Scenario'],
            'names_100': ['100% Domestic Content, Substation (Topside) Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 65,
            'yval_lh': 65
        },
        'Array Cable': {
            'data': [p10['25domEC_UNC'], p10['100domEC_UNC']],
            'data_lh': [p10_lh['25demandEC_LOW'], p10_lh['100demandEC_LOW'], p10_lh['25demandEC_HIGH'], p10_lh['100demandEC_HIGH']],
            'data25':[p10['25domEC_UNC']],
            #'data100':[p10['100domEC_UNC']],
            #'colors_25_100': [colors_list['static_array']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            #'names_25': ['25% Domestic Content, Array Cable Baseline Scenario'],
            #'names_100': ['100% Domestic Content, Array Cable Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 2500,
            'yval_lh': 2250
        },
        'Export Cable': {
            'data': [p11['25domEC_UNC'], p11['100domEC_UNC']],
            'data_lh': [p11_lh['25demandEC_LOW'], p11_lh['100demandEC_LOW'], p11_lh['25demandEC_HIGH'], p11_lh['100demandEC_HIGH']],
            'data100':[p11['100domEC_UNC']],
            'colors_25_100': [colors_list['static_export']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'colors_lh': [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'names_lh': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
            #'names_25': ['25% Domestic Content, Export Cable Baseline Scenario'],
            #'names_100': ['100% Domestic Content, Export Cable Baseline Scenario'],
            'lines': ['dashed','solid'],
            'lines_lh': ['dashed', 'solid', 'dashed', 'solid'],
            'lines25': ['dashed'],
            'lines100':['solid'],
            'yvalmax': 5750,
            'yval_lh': 5800
        }
    }
    #########East coast scenario plots
    # Baseline
    for k, v in scenario_plots.items():
        plot_name = 'Figs/EC_UNC_JobRequirements_'+ k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])
    # Constrained
    for k, v in scenario_plots.items():
        plot_name = 'Figs/EC_LH_JobRequirements_'+ k
        pr.line_plots4(dateYrs, zip(v['data_lh'], v['colors_lh'], v['lines_lh'], v['names_lh']), fname=plot_name, ymax = v['yval_lh'])


    ### Flaoting component demand plots
    scenario_plots_WC = {
        'Nacelle': {
            'data': [p1_fl['25domWC_UNC'], p1_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 14000
        },
        'Rotor Blades': {
            'data': [p2_fl['25domWC_UNC'], p2_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 2500
        },
        'Towers': {
            'data': [p3_fl['25domWC_UNC'], p3_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 3500
        },
        'Floating (turbine)': {
            'data': [p4_fl['25domWC_UNC'], p4_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 25000
        },
        'Floating (floating OSS)': {
            'data': [p5_fl['25domWC_UNC'], p5_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 700
        },
        'Floating OSS Topside': {
            'data': [p6_fl['25domWC_UNC'], p6_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 25
        },
        'Array Cable': {
            'data': [p7_fl['25domWC_UNC'], p7_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 1200
        },
        'Export Cable': {
            'data': [p8_fl['25domWC_UNC'], p8_fl['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed', 'solid'],
            'yvalmax': 2000
        }
    }
    for k, v in scenario_plots_WC.items():
        plot_name = 'Figs/WC_UNC_JobRequirements_' + k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax=v['yvalmax'])

    ### GDP and induced jobs
    # GDP
    yvals_GDP = [totalGDP['Total-Expand GDP']['25GDP_tot_UNC'], totalGDP['Total-Expand GDP']['100GDP_tot_UNC']]
    pr.line_plotsGDP(dateYrs, zip(yvals_GDP, colors_tot, lines_tot, names_tot), fname='Figs/Total_GDP', ymax=10000)
    # Induced jobs
    yvals_GDP = [totalGDP['Total-Expand Induced Impacts']['25GDP_tot_UNC'],
                 totalGDP['Total-Expand Induced Impacts']['100GDP_tot_UNC']]
    pr.line_plotsGDP(dateYrs, zip(yvals_GDP, colors_tot, lines_tot, names_tot), fname='Figs/Induced_jobs',
                     ymax=50000, myylabel='Jobs, Full-Time Equivalents')

    ########Total job requirements for east coast low and high constraints
    # for k, v in scenario_plots_LH.items():
    #     plot_name = 'Figs/EC_WorkforcePipeline_'+ k
    #     pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])

    #####Varied Scenario Job Requirements for east coast
        ##Low vs High constrained

    #####Total direct and indirect jobs for east and west Coast
    #JEDI - Varied Scenarios graphs
    # total_pipeline = 'Total-Expand_Jobs and EC-UNC.xlsx' #Define input spreadsheet
    #
    # total_JEDI = ['Total-Expand Scenario'] #Define sheet to pull from to plot scenarios
    # #data start and end dates
    # dateStrt = 2021
    # dateND = 2033 #2035? - check w/ matt or jeremy
    # dateYears = np.arange(dateStrt, dateND+1)
    #
    # #loop through scenarios
    # ECWCPipeline = {}
    # for s in total_JEDI:
    #     ECWCPipeline[s] = read_varsTot(file=total_pipeline, sheet=s, xrange=dateYears) #read in Excel
    #     #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')

    # print(ECWCPipeline)
    ###Total workforce for baseline scenarios
    ##define variables
    # colors_ecwc = [colors_list['ctv'], colors_list['tugs']]
    # names_ec = ['25% Domestic Content, East Coast Baseline Scenario', '100% Domestic Content, East Coast Baseline Scenario']
    # names_wc = ['25% Domestic Content, West Coast Baseline Scenario', '100% Domestic Content, West Coast Baseline Scenario']
    # lines_ecwc = ['dashed', 'solid']

    #east coast workforce demand
    # yvals_EC = [ECWCPipeline['Total-Expand Scenario']['25demandEC_UNC'], ECWCPipeline['Total-Expand Scenario']['100demandEC_UNC']]
    # pr.line_plots2(dateYrs, zip(yvals_EC, colors_ecwc, lines_ecwc, names_ec), fname='Figs/East_Coast_Workforce_Demand', ymax = 85000)

    #west coast workforce demand
    # yvals_EC = [ECWCPipeline['Total-Expand Scenario']['25demandWC_UNC'],ECWCPipeline['Total-Expand Scenario']['100demandWC_UNC']]
    # pr.line_plots2(dateYrs, zip(yvals_EC, colors_ecwc, lines_ecwc, names_wc), fname='Figs/West_Coast_Workforce_Demand', ymax = 25000)

    # colors_tot = [colors_list['ctv'], colors_list['tugs']]
    # names_tot = ['25% Domestic Content, Total Workforce Baseline Scenario', '100% Domestic Content, Total Workforce Baseline Scenario']
    # lines_tot = ['dashed', 'solid']
    #
    # #Total workforce demand
    # yvals_EC = [ECWCPipeline['Total-Expand Scenario']['25demandTot_UNC'], ECWCPipeline['Total-Expand Scenario']['100demandTot_UNC']]
    # pr.line_plots2(dateYrs, zip(yvals_EC, colors_tot, lines_tot, names_tot), fname='Figs/Total_Workforce_Demand', ymax = 85000)



    #JEDI - Floating Varied Scenarios graphs

    # float_pipeline = 'WC-UNC.xlsx' #Define input spreadsheet
    #
    # scenarios_float = ['WC Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Floating (semisubmersible)', 'Floating (floating OSS)', 'Floating OSS Topside', 'Array Cable', 'Export Cable'] #Define sheet to pull from to plot scenarios
    # #data start and end dates
    # strt = 2021
    # end = 2033 #2035? - check w/ matt or jeremy
    # yrs = np.arange(strt, end+1)
    #
    # #loop through scenarios
    # floatPipeline = {}
    # for s in scenarios_float:
    #     floatPipeline[s] = read_jobvars_WC(file=float_pipeline, sheet=s, xrange=yrs) #read in Excel
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')

    ######### GENERATE PLOTS
    ### Domestic Content via JEDI Model for Baseline Scenario
    # looped plots for jobs
    # f1 = floatPipeline['Nacelle']
    # f2 = floatPipeline['Rotor Blades']
    # f3 = floatPipeline['Towers']
    # f4 = floatPipeline['Floating (semisubmersible)']
    # f5 = floatPipeline['Floating (floating OSS)']
    # f6 = floatPipeline['Floating OSS Topside']
    # f7 = floatPipeline['Array Cable']
    # f8 = floatPipeline['Export Cable']
    #
    # scenario_plots_WC = {
    #     'Nacelle': {
    #         'data': [f1['25domWC_UNC'], f1['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 14000
    #     },
    #     'Rotor Blades': {
    #         'data': [f2['25domWC_UNC'], f2['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 2500
    #     },
    #     'Towers': {
    #         'data': [f3['25domWC_UNC'], f3['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 3500
    #     },
    #     'Floating (turbine)': {
    #         'data': [f4['25domWC_UNC'], f4['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 25000
    #     },
    #     'Floating (floating OSS)': {
    #         'data': [f5['25domWC_UNC'], f5['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 700
    #     },
    #     'Floating OSS Topside': {
    #         'data': [f6['25domWC_UNC'], f6['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 25
    #     },
    #     'Array Cable': {
    #         'data': [f7['25domWC_UNC'], f7['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 1200
    #     },
    #     'Export Cable': {
    #         'data': [f8['25domWC_UNC'], f8['100domWC_UNC']],
    #         'colors': [colors_list['ctv'], colors_list['tugs']],
    #         'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
    #         'lines': ['dashed','solid'],
    #         'yvalmax': 2000
    #     }
    # }
    # for k, v in scenario_plots_WC.items():
    #     plot_name = 'Figs/WC_UNC_JobRequirements_'+ k
    #     pr.line_plots2(yrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])


    # total_GDP = 'Total-Expand_GDP and Induced Impacts.xlsx' #Define input spreadsheet
    #
    # GDP_ECWC = ['Total-Expand GDP', 'Total-Expand Induced Impacts']
    # #data start and end dates
    # # strt1 = 2021
    # # end1 = 2033 #2035? - check w/ matt or jeremy
    # # yrs1 = np.arange(strt, end+1)
    # #loop through scenarios
    # colors_GDP = [colors_list['ctv'], colors_list['tugs']]
    # names_GDP = ['25% Domestic Content, Total Baseline Scenario', '100% Domestic Content, Total Baseline Scenario']
    # lines_GDP = ['dashed', 'solid']
    #
    # totalGDP = {}
    # for s in GDP_ECWC:
    #     totalGDP[s] = read_varsGDP(file=total_GDP, sheet=s, xrange=dateYrs) #read in Excel
    # # GDP
    # yvals_GDP = [totalGDP['Total-Expand GDP']['25GDP_tot_UNC'], totalGDP['Total-Expand GDP']['100GDP_tot_UNC']]
    # pr.line_plotsGDP(dateYrs, zip(yvals_GDP, colors_GDP, lines_GDP, names_GDP), fname='Figs/Total_GDP', ymax = 10000)
    # # Induced jobs
    # yvals_GDP = [totalGDP['Total-Expand Induced Impacts']['25GDP_tot_UNC'], totalGDP['Total-Expand Induced Impacts']['100GDP_tot_UNC']]
    # pr.line_plotsGDP(dateYrs, zip(yvals_GDP, colors_GDP, lines_GDP, names_GDP), fname='Figs/Induced_jobs', ymax = 50000)
