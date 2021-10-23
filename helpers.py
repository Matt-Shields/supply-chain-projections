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

# def create_ITC_tables(df):
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
        _gbf = df.iloc[ind['gbf'], ind['2022col']:ind['2022col']+len(xrange)-1].to_numpy()
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