from pynances import pynance
import os

if __name__ == '__main__':
    # define grouping dictionary for categories
    groupingDict = {
        'Overhead': ['Evil landlord', 'Insurance'],
        'Orderings': ['Amazon', 'Paypal'],
        'Housekeeping': ['Rewe', 'Aldi', 'Real', 'Edeka', 'E-Center', 'Rossmann', 'OBI', 'LIDL'],
        'Gas': ['Aral', 'Esso', 'Shell', 'Total', 'Jet', 'OMV', 'ELO', 'SUPOL'],
        'Income': ['Some Company']}

    # init object, read in files and set categories
    pyn = pynance.Pynance()
    pyn.readCSV(os.getcwd() + r'\example_csvs\example_dkb.csv', 'DKB_giro')
    pyn.readCSV(os.getcwd() + r'\example_csvs\example_consors.csv', 'Consors_giro')
    pyn.setGroups(groupingDict)
    pyn.createMonthlyHTMLReport("example.html")