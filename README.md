# Pynances
Python library to read in bank account csv files and print out some financial graphs.
See [example page](https://cpetry.github.io/pynances/index.html) for an example html output.

- Usable inside python notebooks (jupyter).
- Can generate interactive (javascript) local html pages. 
- Categories can be defined by the user himself.
- Multiple bank accounts can be merged together.
- Annuity loans can be calculated and plotted as graph ouput.

### Security: Every file and every data is processed and displayed locally! 

Categories can be defined like this:
```python
categories = {
    'Overhead'     : ['Evil landlord', 'Insurance'],
    'Orderings'    : ['Amazon', 'Paypal'],
    'Housekeeping' : ['Rewe', 'Aldi', 'Real', 'Edeka', 'E-Center', 'Rossmann', 'OBI', 'LIDL'],
    'Gas'          : ['Aral', 'Esso', 'Shell', 'Total', 'Jet', 'OMV', 'ELO', 'SUPOL'],    
    'Income'       : ['Some Company']}
```

Example graph outputs (plotly) see below:

![Expenses screenshot](https://github.com/cpetry/pynances/blob/master/screenshot_expenses.PNG "Expenses")

![Income screenshot](https://github.com/cpetry/pynances/blob/master/screenshot_income.PNG "Expenses")

See example notebook for usage!
