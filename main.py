"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars, read_jobvars, read_varsTot, read_jobvars_WC, colors_list, read_varsEC, read_varsGDP
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = 'DNV_expanded_pipeline.xlsx'
    # Define scenarios to plot
    scenarios = ['EC-UNC', 'WC-UNC', 'EC-HIGH', 'EC-LOW', 'GBF-UNC', 'FIX-EX','FLOAT-EX']
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
    y2max_turbines = 3000
    y1max_foundations = 450
    y2max_foundations = 3000
    y1max_cables = 2500
    y2max_cables = 16000
    y1max_vessels = 150

    # Baseline
    yvals = [pipeline['EC-UNC']['installMW'], pipeline['WC-UNC']['installMW']]
    colors = [colors_list['fixed'], colors_list['float']]
    names = ['Fixed bottom', 'Floating']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='Figs/baseline_installedMW',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    # Significant supply chain constraints
    yvals_constr = [pipeline['EC-HIGH']['installMW'], pipeline['WC-UNC']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr, colors, names), fname='Figs/constrained_installedMW_high',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    # Moderate supply chain constraints
    yvals_constr_low = [pipeline['EC-LOW']['installMW'], pipeline['WC-UNC']['installMW']]

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
    # for k,v in pipeline['EC-UNC'].items():
    #     expand_install_fixed[k] = np.concatenate(
    #         [v[0:max_ind_fixed], np.repeat(v[max_ind_fixed-1], num_repeat_fixed)])
    # for k, v in pipeline['WC-UNC'].items():
    #     expand_install_float[k] = np.concatenate(
    #         [v[0:max_ind_float], np.repeat(v[max_ind_float - 1], num_repeat_float)])
    # yvals_expand = [expand_install_fixed['installMW'], expand_install_float['installMW']]
    #
    # pr.stacked_bar_cumulative(COD_years, zip(yvals_expand, colors, names), fname='Figs/expanded_installedMW',
    #                           y1max=y1max_deploy, y2max=y2max_deploy)

    # Updated expanded leasing scenarios
    yvals_exp2 = [pipeline['EC-UNC']['installMW'], pipeline['WC-UNC']['installMW'], pipeline['FIX-EX']['installMW'], pipeline['FLOAT-EX']['installMW']]
    colors_exp2 = [colors_list['fixed'], colors_list['float'],colors_list['expand_fix'], colors_list['expand_float']]
    names_exp2 = ['Fixed bottom', 'Floating', 'Expanded fixed bottom leasing', 'Expanded floating leasing']

    pr.stacked_bar_cumulative(COD_years, zip(yvals_exp2, colors_exp2, names_exp2), fname='Figs/expanded2_installedMW',
                              y1max=y1max_deploy, y2max=y2max_deploy)

    ### Number of projects and installation vessels
    # yvals_proj = [pipeline['EC-UNC']['projects'], pipeline['WC-UNC']['projects']]
    # y_vals_wtiv = pipeline['EC-UNC']['wtiv']
    # y_vals_barge= pipeline['EC-UNC']['barge']
    # y_vals_clv = pipeline['EC-UNC']['clv'] + pipeline['WC-UNC']['clv']
    # y_vals_ctv = pipeline['EC-UNC']['ctv'] + pipeline['WC-UNC']['ctv']
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
    y1 = pipeline['EC-UNC']
    y2 = pipeline['WC-UNC']
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
    #y1 = pipeline['EC-UNC']
    #y2 = pipeline['WC-UNC']


    # Significant supply chain constraints
    y1 = pipeline['EC-HIGH']
    y2 = pipeline['WC-UNC']
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
    y2 = pipeline['WC-UNC']
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
    y2 = pipeline['WC-UNC']
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
    # y_EC_berth = pipeline['EC-UNC']
    # y_WC_berth = pipeline['WC-UNC']

    yvals_berths = [pipeline['EC-UNC']['berths']]
    colors_berths = [colors_list['fixed']]
    names_berths = ['Fixed bottom']

    pr.stacked_bar_cumulative(COD_years, zip(yvals_berths, colors_berths, names_berths), fname='Figs/berths',
                              cumulative_line=False)

    #JEDI - Varied Scenarios graphs

    JEDI_pipeline = 'All Scenarios_Varied LC_Jobs.xlsx' #Define input spreadsheet
    JEDI_floating_pipeline = 'WC_Varied LC_Jobs.xlsx'

    scenarios_JEDI = ['Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Monopiles', 'Transition Piece',
                      'Jacket (For Turbine)', 'GBF', 'Jacket (For Substation)', 'Substation (Topside)', 'Array Cable',
                      'Export Cable'] #Define sheet to pull from to plot scenarios
    scenarios_JEDI_floating = ['Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Floating (turbine)', 'Floating (floating OSS)',
                      'Floating OSS Topside', 'Array Cable', 'Export Cable'] #Define sheet to pull from to plot scenarios

    #data start and end dates
    dateStart = 2021
    dateEnd = 2035 #2035? - check w/ matt or jeremy
    dateYrs = np.arange(dateStart, dateEnd+1)

    #loop through scenarios
    EC_jobs_LH = {}
    jobsPipeline = {}
    jobsPipeline_floating = {}
    for s in scenarios_JEDI:
        jobsPipeline[s] = read_jobvars(file=JEDI_pipeline, sheet=s, xrange=dateYrs) #read in Excel
        EC_jobs_LH[s] = read_varsEC(file=JEDI_pipeline, sheet=s, xrange=dateYrs)
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')
    for s in scenarios_JEDI_floating:
        jobsPipeline_floating[s] = read_jobvars_WC(file=JEDI_floating_pipeline, sheet=s, xrange=dateYrs)  # read in Excel

    # print(jobsPipeline_floating)
    ######### GENERATE PLOTS
    ### Domestic Content via JEDI Model for Baseline Scenario
    # looped plots for jobs
    # East coast
    p0 = EC_jobs_LH['Scenarios']
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

    # West Cast
    # p0 = EC_jobs_LH['Scenarios']
    p1_fl = jobsPipeline_floating['Nacelle']
    p2_fl = jobsPipeline_floating['Rotor Blades']
    p3_fl = jobsPipeline_floating['Towers']
    p4_fl = jobsPipeline_floating['Floating (turbine)']
    p5_fl = jobsPipeline_floating['Floating (floating OSS)']
    p6_fl = jobsPipeline_floating['Floating OSS Topside']
    p7_fl = jobsPipeline_floating['Array Cable']
    p8_fl = jobsPipeline_floating['Export Cable']

    scenario_plots_LH = {
        'Low_Scenario': {
        'data': [p0['25demandEC_LOW'], p0['100demandEC_LOW']],
        'colors': [colors_list['ctv'], colors_list['tugs']],
        'names': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints'],
        'lines': ['dashed','solid'],
        'yvalmax': 60000
        },

        'High_Scenario': {
        'data': [p0['25demandEC_HIGH'], p0['100demandEC_HIGH']],
        'colors': [colors_list['ctv'], colors_list['tugs']],
        'names': ['25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
        'lines': ['dashed','solid'],
        'yvalmax': 60000
        }
    }

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
                      'Dynamic array Cable', 'Dynamic export cable']
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
                      'Dynamic array Cable', 'Dynamic export cable']
            # 'names_25': ['25% Domestic Content, Nacelle Baseline Scenario', '25% Domestic Content, Rotor Blades Baseline Scenario', '25% Domestic Content, Towers Baseline Scenario', '25% Domestic Content, Monopiles Baseline Scenario',
            # '25% Domestic Content, Transition Piece Baseline Scenario', '25% Domestic Content, Jacket (For Turbine) Baseline Scenario', '25% Domestic Content, GBF Baseline Scenario', '25% Domestic Content, Jacket (For Substation) Baseline Scenario',
            # '25% Domestic Content, Substation (Topside) Baseline Scenario', '25% Domestic Content, Array Cable Baseline Scenario', '25% Domestic Content, Export Cable Baseline Scenario']
        }
    }

    ###Area plot for Baseline Scenario East Coast Components

    ##Area plot 25% domestic content
    for k, v in workforce_plots.items():
        plot_name = 'Figs/Fixed_JobRequirements_' + k
        pr.area_plotsv2(dateYrs, zip(v['data'], v['colors'], v['names']), fname=plot_name)

    for k, v in workforce_plots_floating.items():
        plot_name = 'Figs/Floating_JobRequirements_' + k
        pr.area_plotsv2(dateYrs, zip(v['data'], v['colors'], v['names']), fname=plot_name)

    scenario_plots = {

        'Nacelle': {
            'data': [p1['25domEC_UNC'], p1['100domEC_UNC']],
            'data_lh': [p1['25domEC_LOW'], p1['100domEC_LOW'], p1['25domEC_HIGH'], p1['100domEC_HIGH']],
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
            'data_lh': [p2['25domEC_LOW'], p2['100domEC_LOW'], p2['25domEC_HIGH'], p2['100domEC_HIGH']],
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
            'data_lh': [p3['25domEC_LOW'], p3['100domEC_LOW'], p3['25domEC_HIGH'], p3['100domEC_HIGH']],
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
            'data_lh': [p4['25domEC_LOW'], p4['100domEC_LOW'], p4['25domEC_HIGH'], p4['100domEC_HIGH']],
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
            'yval_lh': 9500
        },
        'Transition Piece': {
            'data': [p5['25domEC_UNC'], p5['100domEC_UNC']],
            'data_lh': [p5['25domEC_LOW'], p5['100domEC_LOW'], p5['25domEC_HIGH'], p5['100domEC_HIGH']],
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
            'data_lh': [p6['25domEC_LOW'], p6['100domEC_LOW'], p6['25domEC_HIGH'], p6['100domEC_HIGH']],
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
            'data_lh': [p7['25domEC_LOW'], p7['100domEC_LOW'], p7['25domEC_HIGH'], p7['100domEC_HIGH']],
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
            'data_lh': [p8['25domEC_LOW'], p8['100domEC_LOW'], p8['25domEC_HIGH'], p8['100domEC_HIGH']],
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
            'data_lh': [p9['25domEC_LOW'], p9['100domEC_LOW'], p9['25domEC_HIGH'], p9['100domEC_HIGH']],
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
            'data_lh': [p10['25domEC_LOW'], p10['100domEC_LOW'], p10['25domEC_HIGH'], p10['100domEC_HIGH']],
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
            'data_lh': [p11['25domEC_LOW'], p11['100domEC_LOW'], p11['25domEC_HIGH'], p11['100domEC_HIGH']],
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
    for k, v in scenario_plots.items():
        plot_name = 'Figs/EC_UNC_JobRequirements_'+ k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])

    ########Total job requirements for east coast low and high constraints
    for k, v in scenario_plots_LH.items():
        plot_name = 'Figs/EC_WorkforcePipeline_'+ k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])

    #####Varied Scenario Job Requirements for east coast
        ##Low vs High constrained
    for k, v in scenario_plots.items():
        plot_name = 'Figs/EC_LH_JobRequirements_'+ k
        pr.line_plots4(dateYrs, zip(v['data_lh'], v['colors_lh'], v['lines_lh'], v['names_lh']), fname=plot_name, ymax = v['yval_lh'])

    #####Total direct and indirect jobs for east and west Coast
    #JEDI - Varied Scenarios graphs
    total_pipeline = 'East Coast + West Coast.xlsx' #Define input spreadsheet

    total_JEDI = ['Total Jobs EC-WC Job Impact'] #Define sheet to pull from to plot scenarios
    #data start and end dates
    dateStrt = 2021
    dateND = 2035 #2035? - check w/ matt or jeremy
    dateYears = np.arange(dateStrt, dateND+1)

    #loop through scenarios
    ECWCPipeline = {}
    for s in total_JEDI:
        ECWCPipeline[s] = read_varsTot(file=total_pipeline, sheet=s, xrange=dateYears) #read in Excel
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')

    ###Total workforce for baseline scenarios
    ##define variables
    colors_ecwc = [colors_list['ctv'], colors_list['tugs']]
    names_ec = ['25% Domestic Content, East Coast Baseline Scenario', '100% Domestic Content, East Coast Baseline Scenario']
    names_wc = ['25% Domestic Content, West Coast Baseline Scenario', '100% Domestic Content, West Coast Baseline Scenario']
    lines_ecwc = ['dashed', 'solid']

    #east coast workforce demand
    yvals_EC = [ECWCPipeline['Total Jobs EC-WC Job Impact']['25demandEC_UNC'], ECWCPipeline['Total Jobs EC-WC Job Impact']['100demandEC_UNC']]
    pr.line_plots2(dateYrs, zip(yvals_EC, colors_ecwc, lines_ecwc, names_ec), fname='Figs/East_Coast_Workforce_Demand', ymax = 85000)

    #west coast workforce demand
    yvals_EC = [ECWCPipeline['Total Jobs EC-WC Job Impact']['25demandWC_UNC'],ECWCPipeline['Total Jobs EC-WC Job Impact']['100demandWC_UNC']]
    pr.line_plots2(dateYrs, zip(yvals_EC, colors_ecwc, lines_ecwc, names_wc), fname='Figs/West_Coast_Workforce_Demand', ymax = 25000)

    colors_tot = [colors_list['ctv'], colors_list['tugs']]
    names_tot = ['25% Domestic Content, Total Workforce Baseline Scenario', '100% Domestic Content, Total Workforce Baseline Scenario']
    lines_tot = ['dashed', 'solid']

    #Total workforce demand
    yvals_EC = [ECWCPipeline['Total Jobs EC-WC Job Impact']['25demandTot_UNC'], ECWCPipeline['Total Jobs EC-WC Job Impact']['100demandTot_UNC']]
    pr.line_plots2(dateYrs, zip(yvals_EC, colors_tot, lines_tot, names_tot), fname='Figs/Total_Workforce_Demand', ymax = 85000)



    #JEDI - Floating Varied Scenarios graphs

    float_pipeline = 'WC_Varied LC_Jobs.xlsx' #Define input spreadsheet

    scenarios_float = ['Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Floating (turbine)', 'Floating (floating OSS)', 'Floating OSS Topside', 'Array Cable', 'Export Cable'] #Define sheet to pull from to plot scenarios
    #data start and end dates
    strt = 2021
    end = 2035 #2035? - check w/ matt or jeremy
    yrs = np.arange(strt, end+1)

    #loop through scenarios
    floatPipeline = {}
    for s in scenarios_float:
        floatPipeline[s] = read_jobvars_WC(file=float_pipeline, sheet=s, xrange=yrs) #read in Excel
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')

    ######### GENERATE PLOTS
    ### Domestic Content via JEDI Model for Baseline Scenario
    # looped plots for jobs
    f1 = floatPipeline['Nacelle']
    f2 = floatPipeline['Rotor Blades']
    f3 = floatPipeline['Towers']
    f4 = floatPipeline['Floating (turbine)']
    f5 = floatPipeline['Floating (floating OSS)']
    f6 = floatPipeline['Floating OSS Topside']
    f7 = floatPipeline['Array Cable']
    f8 = floatPipeline['Export Cable']

    scenario_plots_WC = {
        'Nacelle': {
            'data': [f1['25domWC_UNC'], f1['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 7000
        },
        'Rotor Blades': {
            'data': [f2['25domWC_UNC'], f2['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 1500
        },
        'Towers': {
            'data': [f3['25domWC_UNC'], f3['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 2000
        },
        'Floating (turbine)': {
            'data': [f4['25domWC_UNC'], f4['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 12000
        },
        'Floating (floating OSS)': {
            'data': [f5['25domWC_UNC'], f5['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 400
        },
        'Floating OSS Topside': {
            'data': [f6['25domWC_UNC'], f6['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 23
        },
        'Array Cable': {
            'data': [f7['25domWC_UNC'], f7['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 700
        },
        'Export Cable': {
            'data': [f8['25domWC_UNC'], f8['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 1500
        }
    }
    for k, v in scenario_plots_WC.items():
        plot_name = 'Figs/WC_UNC_JobRequirements_'+ k
        pr.line_plots2(yrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])


    total_GDP = 'Total GDP.xlsx' #Define input spreadsheet

    GDP_ECWC = ['Total GDP']
    #data start and end dates
    strt1 = 2021
    end1 = 2035 #2035? - check w/ matt or jeremy
    yrs1 = np.arange(strt, end+1)
    #loop through scenarios

    totalGDP = {}
    for s in GDP_ECWC:
        totalGDP[s] = read_varsGDP(file=total_GDP, sheet=s, xrange=yrs1) #read in Excel
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')


    colors_GDP = [colors_list['ctv'], colors_list['tugs']]
    names_GDP = ['25% Domestic Content, Total Baseline Scenario', '100% Domestic Content, Total Baseline Scenario']
    lines_GDP = ['dashed', 'solid']

    #east coast workforce demand
    yvals_GDP = [totalGDP['Total GDP']['25GDP_tot_UNC'], totalGDP['Total GDP']['100GDP_tot_UNC']]
    pr.line_plotsGDP(yrs1, zip(yvals_GDP, colors_GDP, lines_GDP, names_GDP), fname='Figs/Total_GDP', ymax = 10000)

    #west coast workforce demand
