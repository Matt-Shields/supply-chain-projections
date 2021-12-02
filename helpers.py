import pandas as pd
import numpy as np

group_rows = {'# of OSP': 'Delete',
              '# of export cables': 'Delete',
              'Average Max Water Depth, m': 'Delete',
              'Average Rated Power, MW': 'Delete',
              'AverageMin Water Depth, m': 'Delete',
              'HVAC': 'Delete',
              'HVDC': 'Delete',
              'Number of Projects': 'Number of projects',
              'Total # of 12 MW turbines': 'Total number turbines',
              'Total # of 15 MW turbines': 'Total number turbines',
              'Total # of 18 MW turbines': 'Total number turbines',
              'Total Lease Area, Acres': 'Delete',
              'Total Project Capacity, MW': 'Total project capacity, MW',
              'Total cable array length, km': 'Total cable length, km',
              'Total export cable length, km': 'Total cable length, km',
              'array cable length per turbine, km': 'Delete',
              'export cable length, km': 'Delete',
              'substructure: Total OSP jacket, #': 'Delete',
              'substructure: total  monopiles, #': 'Total number of foundations',
              'substructure: total GBF, #\n': 'Total number of foundations',
              'substructure: total jacket, #\n': 'Total number of foundations'
              }

DNV_indices_EC = {
    'installMW': 0,
    'projects': 1,
    'turb': 2,
    'turb12MW': 3,
    'turb15MW': 4,
    'turb18MW': 5,
    'monopiles': 19,
    'gbf': 21,
    'jacketTurb': 22,
    'jacketOSS': 23,
    'array': 27,
    'export': 28,
    'wtiv': 43,
    'barge': 46,
    'ctv': 47,
    'clv': 48,
    'berths': 53,
    'laydown': 54,
    '2022col': 2,
}

DNV_indices_WC = {
    'installMW': 0,
    'projects': 1,
    'turb': 2,
    'turb12MW': 3,
    'turb15MW': 4,
    'turb18MW': 5,
    'semiTurb': 22,
    'semiOSS': 23,
    'array': 27,
    'export': 28,
    'tugs': 37,
    'ahts': 38,
    'ctv': 40,
    'clv': 41,
    'berths': 45,
    'laydown': 46,
    '2022col': 2,
}

Jobs_indices = { #east coast job indicies
    'yr': 0,
    '25domEC_UNC': 1,
    '100domEC_UNC': 2,
    '25domEC_LOW': 6,
    '100domEC_LOW': 7,
    '25domEC_HIGH': 16,
    '100domEC_HIGH': 17,
    '25totEC_UNC': 21,
    '25dirEC_UNC': 22,
    '25indEC_UNC': 23,
    '100totEC_UNC': 24,
    '100dirEC_UNC': 25,
    '100indEC_UNC': 26,
    '25totEC_LOW': 29,
    '25dirEC_LOW': 30,
    '25indEC_LOW': 31,
    '100totEC_LOW': 32,
    '100dirEC_LOW': 33,
    '100indEC_LOW': 34,
    '25totEC_HIGH': 45,
    '25dirEC_HIGH': 46,
    '25indEC_HIGH': 47,
    '100totEC_HIGH': 48,
    '100dirEC_HIGH': 49,
    '100indEC_HIGH': 50,
    '2021col': 1,
}

Jobs_indices_WC = { #west coast job indicies
    'yr': 0,
    '25domWC_UNC': 1,
    '100domWC_UNC': 2,
    '25totWC_UNC': 21,
    '25dirWC_UNC': 22,
    '25indWC_UNC': 23,
    '100totWC_UNC': 24,
    '100dirWC_UNC': 25,
    '100indWC_UNC': 26,
    '2021col': 1,
}

EC_WC_indicies = { #east coast + west coast job indicies for ttoal workforce demand
    'yr': 0,
    '2021col': 1,
    '25demandEC_UNC': 0,
    '100demandEC_UNC': 3,
    '25demandWC_UNC': 7,
    '100demandWC_UNC': 10,
    '25demandTot_UNC': 14,
    '100demandTot_UNC': 17
}

EC_indicies = {
    'yr': 0,
    '2021col': 1,
    '25demandEC_LOW': 33,
    '100demandEC_LOW': 36,
    '25demandEC_MED': 63,
    '100demandEC_MED': 66,
    '25demandEC_HIGH': 95,
    '100demandEC_HIGH': 98
}

GDP_indicies = {
    '2021col': 1,
    '25GDP_EC_UNC': 0,
    '100GDP_EC_UNC': 3,
    '25GDP_WC_UNC': 7,
    '100GDP_WC_UNC': 10,
    '25GDP_tot_UNC': 14,
    '100GDP_tot_UNC': 17
}

colors_list = {
    'fixed': '#0B5E90',
    'float': '#00A4E4',
    'wtiv':'#F7A11A',
    'barge': '#5D9732',
    'clv': '#933C06',
    'ctv': '#5E6A71',
    'tugs': 'k',
    'ahts': 'g',
    '12MW': 'orange',
    '15MW': 'blue',
    '18MW': 'seagreen',
    'static_array': 'olive',
    'static_export': 'steelblue',
    'dynamic_array': 'maroon',
    'dynamic_export': 'darkviolet',
    'monopiles': '#282D30',
    'jackets': 'lightsalmon',
    'gbfs': '#8CC63F',
    'semis': '#5DD2FF',
    'rotors':'firebrick',
    'towers':'rebeccapurple',
    'transp': 'darkorange',
    'jackt_t':'navy',
    'subt':'indigo',
    'berths':'navy',


}

def read_vars(file, sheet, xrange, header=81, cols='B:Q', rows=59, ind=DNV_indices_EC, ind_WC=DNV_indices_WC):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    # Extract all required variables as numpy arrays
    _installMW = df.iloc[ind['installMW'], ind['2022col']:ind['2022col'] + len(xrange) ].to_numpy()
    _projects = df.iloc[ind['projects'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _turb = df.iloc[ind['turb'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _turb12MW = df.iloc[ind['turb12MW'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _turb15MW = df.iloc[ind['turb15MW'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _turb18MW = df.iloc[ind['turb18MW'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _wtiv = df.iloc[ind['wtiv'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _barge = df.iloc[ind['barge'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy() ##TODO: probably going to need a separate call for the different berths
    if 'WC' in sheet:
        # Floating
        _semiTurb = df.iloc[ind_WC['semiTurb'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _semiOSS = df.iloc[ind_WC['semiOSS'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _semi = np.add(_semiTurb, _semiOSS)
        _array = df.iloc[ind_WC['array'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _export = df.iloc[ind_WC['export'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _tugs = df.iloc[ind_WC['tugs'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _ahts = df.iloc[ind_WC['ahts'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _ctv = df.iloc[ind_WC['ctv'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        _clv = df.iloc[ind_WC['clv'], ind_WC['2022col']:ind_WC['2022col'] + len(xrange)].to_numpy()
        #_berths = df.iloc[ind_WC['berths'], ind_WC['2022col']:ind_WC['2022col']+len(xrange)].to_numpy()
        _out = {
                'installMW': _installMW,
                'projects': _projects,
                'turb': _turb,
                'turb12MW': _turb12MW,
                'turb15MW': _turb15MW,
                'turb18MW': _turb18MW,
                'semiTurb': _semiTurb,
                'semiOSS': _semiOSS,
                'semi': _semi,
                'array': _array,
                'export': _export,
                'tugs': _tugs,
                'ahts': _ahts,
                'ctv': _ctv,
                'clv': _clv,
                'berths': _berths,
            }
    else:
        _monopiles = df.iloc[ind['monopiles'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacketTurb = df.iloc[ind['jacketTurb'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacketOSS = df.iloc[ind['jacketOSS'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacket = np.add(_jacketTurb, _jacketOSS)
        _gbf = df.iloc[ind['gbf'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
        _array = df.iloc[ind['array'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _export = df.iloc[ind['export'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _ctv = df.iloc[ind['ctv'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _clv = df.iloc[ind['clv'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        #_berths = df.iloc[ind['berths'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
        _out = {
                'installMW': _installMW,
                'projects': _projects,
                'turb': _turb,
                'turb12MW': _turb12MW,
                'turb15MW': _turb15MW,
                'turb18MW': _turb18MW,
                'monopiles': _monopiles,
                'jacketTurb': _jacketTurb,
                'jacketOSS': _jacketOSS,
                'jacket': _jacket,
                'gbf': _gbf,
                'array': _array,
                'export': _export,
                'wtiv': _wtiv,
                'barge': _barge,
                'ctv': _ctv,
                'clv': _clv,
                #'berths': _berths,
            }
    return _out

#ignore 50%, 75%, and MED scenerios
def read_jobvars(file, sheet, xrange, header=2, cols='B:Q', rows=58, ind=Jobs_indices):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    # Extract all required variables as numpy arrays
    _25domEC_UNC = df.iloc[ind['25domEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100domEC_UNC = df.iloc[ind['100domEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25domEC_LOW = df.iloc[ind['25domEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100domEC_LOW = df.iloc[ind['100domEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25domEC_HIGH = df.iloc[ind['25domEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100domEC_HIGH = df.iloc[ind['100domEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25totEC_UNC = df.iloc[ind['25totEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25dirEC_UNC = df.iloc[ind['25dirEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25indEC_UNC = df.iloc[ind['25indEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100totEC_UNC = df.iloc[ind['100totEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100dirEC_UNC = df.iloc[ind['100dirEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100indEC_UNC = df.iloc[ind['100indEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25totEC_LOW = df.iloc[ind['25totEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25dirEC_LOW = df.iloc[ind['25dirEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25indEC_LOW = df.iloc[ind['25indEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100totEC_LOW = df.iloc[ind['100totEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100dirEC_LOW = df.iloc[ind['100dirEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100indEC_LOW = df.iloc[ind['100indEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25totEC_HIGH = df.iloc[ind['25totEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25dirEC_HIGH = df.iloc[ind['25dirEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25indEC_HIGH = df.iloc[ind['25indEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100totEC_HIGH = df.iloc[ind['100totEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100dirEC_HIGH = df.iloc[ind['100dirEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100indEC_HIGH = df.iloc[ind['100indEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outjobs = {
            '25domEC_UNC' : _25domEC_UNC,
            '100domEC_UNC': _100domEC_UNC,
            '25domEC_LOW' :_25domEC_LOW,
            '100domEC_LOW':_100domEC_LOW,
            '25domEC_HIGH': _25domEC_HIGH,
            '100domEC_HIGH': _100domEC_HIGH,
            '25totEC_UNC': _25totEC_UNC,
            '25dirEC_UNC':_25dirEC_UNC,
            '25indEC_UNC':_25indEC_UNC,
            '100totEC_UNC':_100totEC_UNC,
            '100dirEC_UNC':_100dirEC_UNC,
            '100indEC_UNC':_100indEC_UNC,
            '25totEC_LOW':_25totEC_LOW,
            '25dirEC_LOW':_25dirEC_LOW,
            '25indEC_LOW':_25indEC_LOW,
            '100totEC_LOW':_100totEC_LOW,
            '100dirEC_LOW':_100dirEC_LOW,
            '100indEC_LOW':_100indEC_LOW,
            '25totEC_HIGH':_25totEC_HIGH,
            '25dirEC_HIGH':_25dirEC_HIGH,
            '25indEC_HIGH':_25indEC_HIGH,
            '100totEC_HIGH':_100totEC_HIGH,
            '100dirEC_HIGH':_100dirEC_HIGH,
            '100indEC_HIGH':_100indEC_HIGH
        }
    return _outjobs

def read_varsTot(file, sheet, xrange, header=2, cols='B:Q', rows=24, ind=EC_WC_indicies):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    _25demandEC_UNC = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_UNC = df.iloc[ind['100demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandWC_UNC = df.iloc[ind['25demandWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandWC_UNC = df.iloc[ind['100demandWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandTot_UNC = df.iloc[ind['25demandTot_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandTot_UNC = df.iloc[ind['100demandTot_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outTot = {
            '25demandEC_UNC': _25demandEC_UNC,
            '100demandEC_UNC': _100demandEC_UNC,
            '25demandWC_UNC': _25demandWC_UNC,
            '100demandWC_UNC': _100demandWC_UNC,
            '25demandTot_UNC': _25demandTot_UNC,
            '100demandTot_UNC': _100demandTot_UNC
            }
    return _outTot

def read_varsEC(file, sheet, xrange, header=2, cols='B:Q', rows=150, ind=EC_indicies):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    _25demandEC_LOW = df.iloc[ind['25demandEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_LOW = df.iloc[ind['100demandEC_LOW'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandEC_MED = df.iloc[ind['25demandEC_MED'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_MED = df.iloc[ind['100demandEC_MED'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandEC_HIGH = df.iloc[ind['25demandEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_HIGH = df.iloc[ind['100demandEC_HIGH'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outTotEC = {
            '25demandEC_LOW': _25demandEC_LOW,
            '100demandEC_LOW': _100demandEC_LOW,
            '25demandEC_MED': _25demandEC_MED,
            '100demandEC_MED': _100demandEC_MED,
            '25demandEC_HIGH': _25demandEC_HIGH,
            '100demandEC_HIGH': _100demandEC_HIGH
            }
    return _outTotEC

#ignore 50%, 75%, and MED scenerios
def read_jobvars_WC(file, sheet, xrange, header=2, cols='B:Q', rows=58, ind=Jobs_indices_WC):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    # Extract all required variables as numpy arrays
    _25domWC_UNC = df.iloc[ind['25domWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100domWC_UNC = df.iloc[ind['100domWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25totWC_UNC = df.iloc[ind['25totWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25dirWC_UNC = df.iloc[ind['25dirWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25indWC_UNC = df.iloc[ind['25indWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100totWC_UNC = df.iloc[ind['100totWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100dirWC_UNC = df.iloc[ind['100dirWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100indWC_UNC = df.iloc[ind['100indWC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outjobsWC = {
            '25domWC_UNC' : _25domWC_UNC,
            '100domWC_UNC': _100domWC_UNC,
            '25totWC_UNC': _25totWC_UNC,
            '25dirWC_UNC':_25dirWC_UNC,
            '25indWC_UNC':_25indWC_UNC,
            '100totWC_UNC':_100totWC_UNC,
            '100dirWC_UNC':_100dirWC_UNC,
            '100indWC_UNC':_100indWC_UNC,
        }
    return _outjobsWC

def read_varsGDP(file, sheet, xrange, header=2, cols='B:Q', rows=36, ind=GDP_indicies):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    _25GDP_EC_UNC = df.iloc[ind['25GDP_EC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100GDP_EC_UNC = df.iloc[ind['100GDP_EC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25GDP_WC_UNC = df.iloc[ind['25GDP_WC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100GDP_WC_UNC = df.iloc[ind['100GDP_WC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25GDP_tot_UNC = df.iloc[ind['25GDP_tot_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100GDP_tot_UNC = df.iloc[ind['100GDP_tot_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outGDP = {
            '25GDP_EC_UNC': _25GDP_EC_UNC,
            '100GDP_EC_UNC': _100GDP_EC_UNC,
            '25GDP_WC_UNC': _25GDP_WC_UNC,
            '100GDP_WC_UNC': _100GDP_WC_UNC,
            '25GDP_tot_UNC': _25GDP_tot_UNC,
            '100GDP_tot_UNC': _100GDP_tot_UNC
            }

    return _outGDP
