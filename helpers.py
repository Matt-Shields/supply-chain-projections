import pandas as pd

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


# def create_ITC_tables(df):
