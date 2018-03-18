import json
import os, sys
from pynances import pynance

if __name__ == '__main__':

    configFile = 'config.cfg' if len(sys.argv) <= 1 else sys.argv[1]
    config = json.load(open(configFile))

    pyn = pynance.Pynance()

    for type, filepath  in config['csvFiles']:
        if not os.path.exists(filepath):
            pyn.readCSV(os.getcwd() + filepath, type)
        else:
            pyn.readCSV(filepath, type)

    pyn.setGroups(config['categories'])
    pyn.createMonthlyHTMLReport(config["output"])