"""Plotting routines for supply chain and workforce projections"""

import numpy as np
import pandas as pd
import plot_routines as pr
from helpers import group_rows, read_vars, read_jobvars, read_varsTot, read_jobvars_WC, colors_list, read_varsEC
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Define input spreadsheet
    DNV_gantt = 'DNV_pipelines_v2.xlsm'
    # Define scenarios to plot
    scenarios = ['EC-UNC', 'WC-UNC', 'EC-HIGH', 'EC-LOW', 'GBF-UNC']
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
    # Baseline
    yvals = [pipeline['EC-UNC']['installMW'], pipeline['WC-UNC']['installMW']]
    colors = [colors_list['fixed'], colors_list['float']]
    names = ['Fixed bottom', 'Floating']

    pr.stacked_bar_cumulative(COD_years, zip(yvals, colors, names), fname='Figs/baseline_installedMW', y1max=10000, y2max=40000)

    # Significant supply chain constraints
    yvals_constr = [pipeline['EC-HIGH']['installMW'], pipeline['WC-UNC']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr, colors, names), fname='Figs/constrained_installedMW_high', y1max=10000, y2max=40000)

    # Moderate supply chain constraints
    yvals_constr_low = [pipeline['EC-LOW']['installMW'], pipeline['WC-UNC']['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_constr_low, colors, names), fname='Figs/constrained_installedMW_low',
                              y1max=10000, y2max=40000)

    # Constant throughput after 2029
    # Extend out baseline scenarios
    max_ind_fixed = 7  # 2028 - max fixed deployment
    max_ind_float = 8  # 2029 - max floating deployment
    num_repeat_fixed = len(COD_years) - max_ind_fixed
    num_repeat_float = len(COD_years) - max_ind_float

    # expand_install_fixed = np.concatenate([pipeline['EC-UNCONSTR']['installMW'][0:max_ind_fixed],
    #                                        np.repeat(pipeline['EC-UNCONSTR']['installMW'][max_ind_fixed-1], num_repeat_fixed)])
    # expand_install_float = np.concatenate([pipeline['WC-UNC']['installMW'][0:max_ind_float],
    #                                        np.repeat(pipeline['WC-UNC']['installMW'][max_ind_float-1], num_repeat_float)])
    expand_install_fixed = {}
    expand_install_float = {}
    for k,v in pipeline['EC-UNC'].items():
        expand_install_fixed[k] = np.concatenate(
            [v[0:max_ind_fixed], np.repeat(v[max_ind_fixed-1], num_repeat_fixed)])
    for k, v in pipeline['WC-UNC'].items():
        expand_install_float[k] = np.concatenate(
            [v[0:max_ind_float], np.repeat(v[max_ind_float - 1], num_repeat_float)])
    yvals_expand = [expand_install_fixed['installMW'], expand_install_float['installMW']]

    pr.stacked_bar_cumulative(COD_years, zip(yvals_expand, colors, names), fname='Figs/expanded_installedMW', y1max=10000)

    ### Number of projects and installation vessels
    yvals_proj = [pipeline['EC-UNC']['projects'], pipeline['WC-UNC']['projects']]
    y_vals_wtiv = pipeline['EC-UNC']['wtiv']
    y_vals_barge= pipeline['EC-UNC']['barge']
    y_vals_clv = pipeline['EC-UNC']['clv'] + pipeline['WC-UNC']['clv']
    y_vals_ctv = pipeline['EC-UNC']['ctv'] + pipeline['WC-UNC']['ctv']

    y_vessels = [y_vals_wtiv, y_vals_barge, y_vals_clv, y_vals_ctv]
    vessel_colors = [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv']]
    vessel_names = ['WTIV', 'Feeder barge', 'CLV', 'CTV']

    pr.stacked_bar_line(COD_years, zip(yvals_proj, colors, names), zip(y_vessels, vessel_colors, vessel_names),
                        fname='Figs/baseline_proj_vessels', myylabel='Installed projects', myy2label='Number of vessels')

    #### Add for other scenarios

    ### Line plots for individual components
    # Baseline
    y1 = pipeline['EC-UNC']
    y2 = pipeline['WC-UNC']
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of Turbines'
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of Foundations'
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of Cable, km'
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of Vessels'
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/baseline_component_' + k
        pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                  myylabel=v['ylabel'], myy2label='Cumulative ' +v['ylabel'])

    # Significant supply chain constraints
    y1 = pipeline['EC-HIGH']
    y2 = pipeline['WC-UNC']
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines'
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations'
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km'
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of Vessels'
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/constrained_high_component_'+ k
        pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                  myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'])

    # Moderate supply chain constraints
    y1 = pipeline['EC-LOW']
    y2 = pipeline['WC-UNC']
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines'
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations'
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km'
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of Vessels'
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/constrained_low_component_'+ k
        pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                  myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'])

    # Expanded pipeline
    y1 = expand_install_fixed
    y2 = expand_install_float
    component_plots = {
        'Turbines': {
                    'data': [y1['turb12MW']+y2['turb12MW'], y1['turb15MW']+y2['turb15MW'], y1['turb18MW']+y2['turb18MW']],
                    'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
                    'names': [ '12MW', '15MW','18MW'],
                    'ylabel': 'Number of turbines'
                    },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations'
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'], colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km'
        },
        'Vessels':{
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of Vessels'
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/expanded_component_'+ k
        pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                  myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'])

    # GBF market share
    y1 = pipeline['GBF-UNC']
    y2 = pipeline['WC-UNC']
    component_plots = {
        'Turbines': {
            'data': [y1['turb12MW'] + y2['turb12MW'], y1['turb15MW'] + y2['turb15MW'], y1['turb18MW'] + y2['turb18MW']],
            'colors': [colors_list['12MW'], colors_list['15MW'], colors_list['18MW']],
            'names': ['12MW', '15MW', '18MW'],
            'ylabel': 'Number of turbines'
        },
        'Foundations': {
            'data': [y1['monopiles'], y1['jacket'], y1['gbf'], y2['semi']],
            'colors': [colors_list['monopiles'], colors_list['jackets'], colors_list['gbfs'], colors_list['semis']],
            'names': ['Monopiles', 'Jackets', 'GBFs', 'Semisubmersibles'],
            'ylabel': 'Number of foundations'
        },
        'Cables': {
            'data': [y1['array'], y1['export'], y2['array'], y2['export']],
            'colors': [colors_list['static_array'], colors_list['static_export'], colors_list['dynamic_array'],
                       colors_list['dynamic_export']],
            'names': ['Static array cables', 'Static export cables', 'Dynamic array cables', 'Dynamic export cables'],
            'ylabel': 'Length of cable, km'
        },
        'Vessels': {
            'data': [y1['wtiv'], y1['barge'], y1['clv']+y2['clv'], y1['ctv']+y2['ctv'], y2['tugs'], y2['ahts']],
            'colors': [colors_list['wtiv'], colors_list['barge'], colors_list['clv'], colors_list['ctv'], colors_list['tugs'], colors_list['ahts']],
            'names': ['WTIV', 'Feeder barge', 'CLV', 'CTV', 'Tugboats','AHTS'],
            'ylabel': 'Number of Vessels'
        }
    }

    for k, v in component_plots.items():
        plot_name = 'Figs/uniform_found_component_'+ k
        pr.stacked_bar_cumulative(COD_years, zip(v['data'], v['colors'], v['names']), fname=plot_name,
                                  myylabel=v['ylabel'], myy2label='Cumulative ' + v['ylabel'])


    #JEDI - Varied Scenarios graphs

    JEDI_pipeline = 'All Scenarios_Varied LC_Jobs.xlsx' #Define input spreadsheet

    scenarios_JEDI = ['Scenarios', 'Nacelle', 'Rotor Blades', 'Towers', 'Monopiles', 'Transition Piece', 'Jacket (For Turbine)', 'GBF', 'Jacket (For Substation)', 'Substation (Topside)', 'Array Cable', 'Export Cable'] #Define sheet to pull from to plot scenarios
    #data start and end dates
    dateStart = 2021
    dateEnd = 2035 #2035? - check w/ matt or jeremy
    dateYrs = np.arange(dateStart, dateEnd+1)

    #loop through scenarios
    EC_jobs_LH = {}
    jobsPipeline = {}
    for s in scenarios_JEDI:
        jobsPipeline[s] = read_jobvars(file=JEDI_pipeline, sheet=s, xrange=dateYrs) #read in Excel
        EC_jobs_LH[s] = read_varsEC(file=JEDI_pipeline, sheet=s, xrange=dateYrs)
        #line_plots2(x, y_zip,  fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year')

    ######### GENERATE PLOTS
    ### Domestic Content via JEDI Model for Baseline Scenario
    # looped plots for jobs
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

    scenario_plots_LH = {
        'Low_Scenario': {
        'data': [p0['25demandEC_LOW'], p0['100demandEC_LOW']],
        'colors': [colors_list['static_export'], colors_list['fixed']],
        'names': ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints'],
        'lines': ['dashed','solid'],
        'yvalmax': 60000
        },

        'High_Scenario': {
        'data': [p0['25demandEC_HIGH'], p0['100demandEC_HIGH']],
        'colors': [colors_list['static_export'], colors_list['fixed']],
        'names': ['25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints'],
        'lines': ['dashed','solid'],
        'yvalmax': 60000
        }
    }
    scenario_plots = {

        'Nacelle': {
            'data': [p1['25domEC_UNC'], p1['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 35000
        },
        'Rotor Blades': {
            'data': [p2['25domEC_UNC'], p2['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 6000
        },
        'Towers': {
            'data': [p3['25domEC_UNC'], p3['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 8050
        },
        'Monopiles': {
            'data': [p4['25domEC_UNC'], p4['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 8750
        },
        'Transition Piece': {
            'data': [p5['25domEC_UNC'], p5['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 5000
        },
        'Jacket (For Turbine)': {
            'data': [p6['25domEC_UNC'], p6['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 5000
        },
        'GBF': {
            'data': [p7['25domEC_UNC'], p7['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 8500
        },
        'Jacket (For Substation)': {
            'data': [p8['25domEC_UNC'], p8['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 80
        },
        'Substation (Topside)': {
            'data': [p9['25domEC_UNC'], p9['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 65
        },
        'Array Cable': {
            'data': [p10['25domEC_UNC'], p10['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 2500
        },
        'Export Cable': {
            'data': [p11['25domEC_UNC'], p11['100domEC_UNC']],
            'colors': [colors_list['static_export'], colors_list['fixed']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 5500
        }
    }
    for k, v in scenario_plots.items():
        plot_name = 'Figs/EC_UNC_JobRequirements_'+ k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])

    for k, v in scenario_plots_LH.items():
        plot_name = 'Figs/EC_WorkforcePipeline_'+ k
        pr.line_plots2(dateYrs, zip(v['data'], v['colors'], v['lines'], v['names']), fname=plot_name, ymax = v['yvalmax'])


    #####Varied Scenario Job Requirements
    ##Low vs High constrained

    #Nacelle Low and High constrained scenarios
    yvals_nac_lh = [jobsPipeline['Nacelle']['25domEC_LOW'], jobsPipeline['Nacelle']['100domEC_LOW'], jobsPipeline['Nacelle']['25domEC_HIGH'], jobsPipeline['Nacelle']['100domEC_HIGH']]
    colors_lh = [colors_list['clv'], colors_list['clv'], colors_list['wtiv'], colors_list['wtiv']]
    names_lh = ['25% Domestic Content, Moderate Supply Constraints', '100% Domestic Content, Moderate Supply Constraints', '25% Domestic Content, Significant Supply Constraints', '100% Domestic Content, Significant Supply Constraints']
    lines_lh = ['dashed', 'solid', 'dashed', 'solid']

    pr.line_plots4(dateYrs, zip(yvals_nac_lh, colors_lh, lines_lh, names_lh), fname='Figs/Nacelle_Job_Requirements_ECLH', ymax=35000)

    #Rotor Blades Low and High East Coast
    yvals_blades_lh = [jobsPipeline['Rotor Blades']['25domEC_LOW'], jobsPipeline['Rotor Blades']['100domEC_LOW'], jobsPipeline['Rotor Blades']['25domEC_HIGH'], jobsPipeline['Rotor Blades']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_blades_lh, colors_lh, lines_lh, names_lh), fname='Figs/Blades_Job_Requirements_ECLH', ymax=6000)

    #Tower Low and High East Coast
    yvals_tower_lh = [jobsPipeline['Towers']['25domEC_LOW'], jobsPipeline['Towers']['100domEC_LOW'], jobsPipeline['Towers']['25domEC_HIGH'], jobsPipeline['Towers']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_tower_lh, colors_lh, lines_lh, names_lh), fname='Figs/Tower_Job_Requirements_ECLH', ymax=8050)

    #Transition Piece Low and High East Coast
    yvals_tp_lh = [jobsPipeline['Transition Piece']['25domEC_LOW'], jobsPipeline['Transition Piece']['100domEC_LOW'], jobsPipeline['Transition Piece']['25domEC_HIGH'], jobsPipeline['Transition Piece']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_tp_lh, colors_lh, lines_lh, names_lh), fname='Figs/Transition_Piece_Job_Requirements_ECLH', ymax=5000)

    #Jacket (For Turbine) Low and High East Coast
    yvals_jacket_lh = [jobsPipeline['Jacket (For Turbine)']['25domEC_LOW'], jobsPipeline['Jacket (For Turbine)']['100domEC_LOW'], jobsPipeline['Jacket (For Turbine)']['25domEC_HIGH'], jobsPipeline['Jacket (For Turbine)']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_jacket_lh, colors_lh, lines_lh, names_lh), fname='Figs/Turbine_Jacket_Job_Requirements_ECLH', ymax=5000)

    #Monopiles Low and High East Coast
    yvals_mono_lh = [jobsPipeline['Monopiles']['25domEC_LOW'], jobsPipeline['Monopiles']['100domEC_LOW'], jobsPipeline['Monopiles']['25domEC_HIGH'], jobsPipeline['Monopiles']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_mono_lh, colors_lh, lines_lh, names_lh), fname='Figs/Monopiles_Job_Requirements_ECLH', ymax=8750)

    #GBF Low and High East Coast
    yvals_GBF_lh = [jobsPipeline['GBF']['25domEC_LOW'], jobsPipeline['GBF']['100domEC_LOW'], jobsPipeline['GBF']['25domEC_HIGH'], jobsPipeline['GBF']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_GBF_lh, colors_lh, lines_lh, names_lh), fname='Figs/GBF_Job_Requirements_ECLH', ymax=8500)

    #Jacket (For Substation) and High East Coast
    yvals_subj_lh = [jobsPipeline['Jacket (For Substation)']['25domEC_LOW'], jobsPipeline['Jacket (For Substation)']['100domEC_LOW'], jobsPipeline['Jacket (For Substation)']['25domEC_HIGH'], jobsPipeline['Jacket (For Substation)']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_subj_lh, colors_lh, lines_lh, names_lh), fname='Figs/Substation_Jacket_Job_Requirements_ECLH', ymax=85)

    #Substation (Topside) Low and High East Coast
    yvals_subt_lh = [jobsPipeline['Substation (Topside)']['25domEC_LOW'], jobsPipeline['Substation (Topside)']['100domEC_LOW'], jobsPipeline['Substation (Topside)']['25domEC_HIGH'], jobsPipeline['Substation (Topside)']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_subt_lh, colors_lh, lines_lh, names_lh), fname='Figs/Substation_Topside_Job_Requirements_ECLH', ymax=60)

    #Array Cable Low and High East Coast
    yvals_array_lh = [jobsPipeline['Array Cable']['25domEC_LOW'], jobsPipeline['Array Cable']['100domEC_LOW'], jobsPipeline['Array Cable']['25domEC_HIGH'], jobsPipeline['Array Cable']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_array_lh, colors_lh, lines_lh, names_lh), fname='Figs/Array_Cable_Job_Requirements_ECLH', ymax=2500)

    #Export Cable Low and High East Coast
    yvals_export_lh = [jobsPipeline['Export Cable']['25domEC_LOW'], jobsPipeline['Export Cable']['100domEC_LOW'], jobsPipeline['Export Cable']['25domEC_HIGH'], jobsPipeline['Export Cable']['100domEC_HIGH']]
    pr.line_plots4(dateYrs, zip(yvals_export_lh, colors_lh, lines_lh, names_lh), fname='Figs/Export_Cable_Job_Requirements_ECLH', ymax=5500)



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
    pr.line_plots2(dateYrs, zip(yvals_EC, colors_ecwc, lines_ecwc, names_wc), fname='Figs/West_Coast_Workforce_Demand', ymax = 30000)

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
            'yvalmax': 6000
        },
        'Rotor Blades': {
            'data': [f2['25domWC_UNC'], f2['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 1000
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
            'yvalmax': 10250
        },
        'Floating (floating OSS)': {
            'data': [f5['25domWC_UNC'], f5['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 350
        },
        'Floating OSS Topside': {
            'data': [f6['25domWC_UNC'], f6['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 25
        },
        'Array Cable': {
            'data': [f7['25domWC_UNC'], f7['100domWC_UNC']],
            'colors': [colors_list['ctv'], colors_list['tugs']],
            'names': ['25% Domestic Content, Baseline Scenario', '100% Domestic Content, Baseline Scenario'],
            'lines': ['dashed','solid'],
            'yvalmax': 600
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
