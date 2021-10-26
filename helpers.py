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

DNV_indices = {
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
    'semiTurb': 22,
    'semiOSS': 23,
    'array': 27,
    'export': 28,
    'wtiv': 43,
    'barge': 46,
    'ctv': 47,
    'clv': 48,
    'berths': 53,
    '2022col': 2,
}

Jobs_indices = {
    'yr': 0,
    '25domEC_UNC': 2,
    '100domEC_UNC': 3,
    '25domEC_LOW': 7,
    '100domEC_LOW': 8,
    '25domEC_HIGH': 17,
    '100domEC_HIGH': 18,
    '25totEC_UNC': 22,
    '25dirEC_UNC': 23,
    '25indEC_UNC': 24,
    '100totEC_UNC': 25,
    '100dirEC_UNC': 26,
    '100indEC_UNC': 27,
    '25totEC_LOW': 30,
    '25dirEC_LOW': 31,
    '25indEC_LOW': 32,
    '100totEC_LOW': 33,
    '100dirEC_LOW': 34,
    '100indEC_LOW': 35,
    '25totEC_HIGH': 46,
    '25dirEC_HIGH': 47,
    '25indEC_HIGH': 48,
    '100totEC_HIGH': 49,
    '100dirEC_HIGH': 50,
    '100indEC_HIGH': 51,
    '2021col': 1,
    '25demandEC_UNC': 4,
    '100demandEC_UNC': 7,
    '25demandEC_LOW': 36,
    '100demandEC_LOW': 39,
    '25demandEC_HIGH': 98,
    '100demandEC_HIGH': 101,
    '25demandGBF_UNC': 130,
    '100demandGBF_UNC': 133
}


colors_list = {
    'fixed': '#0B5E90',
    'float': '#00A4E4',
    'wtiv':'#F7A11A',
    'barge': '#5D9732',
    'clv': '#933C06',
    'ctv': '#5E6A71',
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
    'semis': '#5DD2FF'
}

def read_vars(file, sheet, xrange, header=81, cols='B:Q', rows=56, ind=DNV_indices):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    # Extract all required variables as numpy arrays
    _installMW = df.iloc[ind['installMW'], ind['2022col']:ind['2022col'] + len(xrange) ].to_numpy()
    _projects = df.iloc[ind['projects'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _turb = df.iloc[ind['turb'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _turb12MW = df.iloc[ind['turb12MW'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _turb15MW = df.iloc[ind['turb15MW'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _turb18MW = df.iloc[ind['turb18MW'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    _wtiv = df.iloc[ind['wtiv'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _barge = df.iloc[ind['barge'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _ctv = df.iloc[ind['ctv'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    _clv = df.iloc[ind['clv'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
    # _berths = df.iloc[ind['berths'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
    if 'WC' in sheet:
        # Floating
        _semiTurb = df.iloc[ind['semiTurb'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _semiOSS = df.iloc[ind['semiOSS'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _semi = np.add(_semiTurb, _semiOSS)
        _array = df.iloc[ind['array'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _export = df.iloc[ind['export'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
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
                'wtiv': _wtiv,
                'barge': _barge,
                'ctv': _ctv,
                'clv': _clv,
            }
    else:
        _monopiles = df.iloc[ind['monopiles'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacketTurb = df.iloc[ind['jacketTurb'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacketOSS = df.iloc[ind['jacketOSS'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _jacket = np.add(_jacketTurb, _jacketOSS)
        _gbf = df.iloc[ind['gbf'], ind['2022col']:ind['2022col']+len(xrange)].to_numpy()
        _array = df.iloc[ind['array'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
        _export = df.iloc[ind['export'], ind['2022col']:ind['2022col'] + len(xrange)].to_numpy()
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

def read_varsScen(file, sheet, xrange, header=3, cols='B:Q', rows=136, ind=Jobs_indices):
    df = pd.read_excel(file, sheet_name=sheet, header=header, usecols=cols, nrows=rows)
    _25demandEC_UNC = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_UNC = df.iloc[ind['100demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandEC_LOW = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_LOW = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandEC_HIGH = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandEC_HIGH = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _25demandGBF_UNC = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _100demandGBF_UNC  = df.iloc[ind['25demandEC_UNC'], ind['2021col']:ind['2021col'] + len(xrange) ].to_numpy()
    _outScen = {
            '25demandEC_UNC': _25demandEC_UNC,
            '100demandEC_UNC': _100demandEC_UNC,
            '25demandEC_LOW': _25demandEC_LOW,
            '100demandEC_LOW': _100demandEC_LOW,
            '25demandEC_HIGH': _25demandEC_HIGH,
            '100demandEC_HIGH': _100demandEC_HIGH,
            '25demandGBF_UNC': _25demandGBF_UNC,
            '100demandGBF_UNC': _100demandGBF_UNC
            }
    return _outScen

#ignore 50%, 75%, and MED scenerios
