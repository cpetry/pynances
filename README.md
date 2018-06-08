# Pynances
Python library to read in bank account csv files and print out some financial graphs.

## See [example page](https://cpetry.github.io/pynances/example.html) for an example html output!

### Features:
- Usable inside python notebooks (jupyter).
- Can generate interactive (javascript) local html pages. 
- Categories can be defined by the user himself.
- Multiple bank accounts can be merged together.
- Annuity loans can be calculated and plotted as graph ouput.

### Security: Every file and every data is processed and displayed locally! 

### Configuration

The **config.cfg** file can be setup for your own requirements. 

Files to be read in:
```json
"csvFiles": [
		["DKB_giro", "/example_csvs/example_dkb.csv"],
		["Consors_giro", "/example_csvs/example_consors.csv"]
	],
```

Categories can be defined like this:
```json
"categories": {
		"Overhead": ["Evil landlord", "Insurance"],
        "Orderings": ["Amazon", "Paypal"],
        "Housekeeping": ["Rewe", "Aldi", "Real", "Edeka", "E-Center", "Rossmann", "OBI", "LIDL"],
        "Gas": ["Aral", "Esso", "Shell", "Total", "Jet", "OMV", "ELO", "SUPOL"],
        "Income": ["Some Company"]
	},
```

The output file is by default:
```json
"output": "example.html"
```

### Example graph outputs (plotly):

![Expenses screenshot](https://cpetry.github.io/pynances/screenshot_expenses.PNG "Expenses")

![Income screenshot](https://cpetry.github.io/pynances/screenshot_income.PNG "Expenses")

See example notebook for usage!
